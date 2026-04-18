"""QR code generation with circular dot styling and optional center logos."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any

import qrcode
import qrcode.constants
from PIL import Image, ImageDraw


class QRGenerator:
    """Generate high-resolution QR codes with circular dot styling.

    Parameters
    ----------
    data : str
        Text or URL to encode.
    filename : str or Path, optional
        Output file path. Format is inferred from the extension
        (``.png`` or ``.pdf``), by default ``"custom_qr.png"``.
    size : int, optional
        Target image size in pixels, by default 1200. Values below 800
        may produce blurry dots.
    qr_color : str, optional
        Primary dot color as a hex string, by default ``"#000000"``.
    qr_color2 : str or None, optional
        Secondary dot color for random two-color variation. When set,
        each dot is independently assigned one of the two colors.
        ``None`` disables variation, by default ``None``.
    bg_color : str, optional
        Background color as a hex string. Ignored when
        ``transparent_bg=True``, by default ``"#FFFFFF"``.
    center_image_path : str or Path or None, optional
        Path to a logo placed at the center of the QR code, by default
        ``None``.
    logo_size_ratio : float, optional
        Logo width as a fraction of the total image size, by default
        ``1/6`` (~16.7 %).
    dot_size_ratio : float, optional
        Dot diameter relative to the module size (0.1-1.0), by default
        ``0.8``.
    border_modules : int, optional
        Quiet-zone width in modules, by default ``4``.
    transparent_bg : bool, optional
        Render with a transparent background. Requires PNG output and
        ``transparent_bg=False`` for PDF, by default ``False``.
    random_seed : int or None, optional
        Seed for reproducible two-color patterns, by default ``None``.
    """

    def __init__(
        self,
        data: str,
        filename: str | Path = "custom_qr.png",
        size: int = 1200,
        qr_color: str = "#000000",
        qr_color2: str | None = None,
        bg_color: str = "#FFFFFF",
        center_image_path: str | Path | None = None,
        logo_size_ratio: float = 1 / 6,
        dot_size_ratio: float = 0.8,
        border_modules: int = 4,
        transparent_bg: bool = False,
        random_seed: int | None = None,
    ) -> None:
        self.data = data
        self.filename = Path(filename)
        self.size = size
        self.qr_color = qr_color
        self.qr_color2 = qr_color2
        self.bg_color = bg_color
        self.center_image_path = Path(center_image_path) if center_image_path else None
        self.logo_size_ratio = logo_size_ratio
        self.dot_size_ratio = dot_size_ratio
        self.border_modules = border_modules
        self.transparent_bg = transparent_bg
        self.random_seed = random_seed

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate(self) -> Path:
        """Generate the QR code and save it to :attr:`filename`.

        Returns
        -------
        Path
            Absolute path to the saved file.

        Raises
        ------
        FileNotFoundError
            If :attr:`center_image_path` is set but does not exist on disk.
        ValueError
            If ``.pdf`` output is requested together with
            ``transparent_bg=True``.
        """
        self.filename.parent.mkdir(parents=True, exist_ok=True)

        if self.center_image_path and not self.center_image_path.exists():
            raise FileNotFoundError(f"Logo file not found: {self.center_image_path}")

        if self.random_seed is not None:
            random.seed(self.random_seed)

        qr_matrix = self._build_qr_matrix()
        module_count = len(qr_matrix)
        module_size = max(self.size // module_count, 8)
        actual_size = module_size * module_count

        print(
            f"QR: {module_count}x{module_count} modules, "
            f"{module_size}px/module, {actual_size}x{actual_size}px total"
        )

        img = self._create_canvas(actual_size)
        img = self._draw_dots(img, qr_matrix, module_size)

        if self.center_image_path:
            img = self._overlay_logo(img, actual_size)

        return self._save(img)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_qr_matrix(self) -> list[list[bool]]:
        """Build the boolean module matrix for the QR code.

        Returns
        -------
        list[list[bool]]
            Square 2-D matrix where ``True`` marks a filled module.
        """
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=1,
            border=self.border_modules,
        )
        qr.add_data(self.data)
        qr.make(fit=True)
        return qr.get_matrix()  # type: ignore[no-any-return]

    def _create_canvas(self, actual_size: int) -> Image.Image:
        """Create a blank PIL canvas at the computed pixel dimensions.

        Parameters
        ----------
        actual_size : int
            Side length of the square canvas in pixels.

        Returns
        -------
        Image.Image
            Blank ``RGBA`` (transparent) or ``RGB`` (solid) image.
        """
        if self.transparent_bg:
            return Image.new("RGBA", (actual_size, actual_size), (0, 0, 0, 0))
        return Image.new("RGB", (actual_size, actual_size), self.bg_color)

    def _draw_dots(
        self,
        img: Image.Image,
        qr_matrix: list[list[bool]],
        module_size: int,
    ) -> Image.Image:
        """Draw a filled circle for every active QR module.

        Parameters
        ----------
        img : Image.Image
            Canvas to draw on.
        qr_matrix : list[list[bool]]
            Module matrix from :meth:`_build_qr_matrix`.
        module_size : int
            Pixel size of a single module.

        Returns
        -------
        Image.Image
            Canvas with all QR dots rendered.
        """
        module_count = len(qr_matrix)
        dot_radius = (module_size * self.dot_size_ratio) / 2
        colors: list[str] = [self.qr_color, self.qr_color2] if self.qr_color2 else [self.qr_color]

        draw = ImageDraw.Draw(img)
        for row in range(module_count):
            for col in range(module_count):
                if qr_matrix[row][col]:
                    cx = col * module_size + module_size // 2
                    cy = row * module_size + module_size // 2
                    color = random.choice(colors)
                    draw.ellipse(
                        [cx - dot_radius, cy - dot_radius, cx + dot_radius, cy + dot_radius],
                        fill=color,
                    )
        return img

    def _overlay_logo(self, img: Image.Image, actual_size: int) -> Image.Image:
        """Composite the center logo onto the QR image.

        Parameters
        ----------
        img : Image.Image
            Rendered QR code image.
        actual_size : int
            Side length of ``img`` in pixels.

        Returns
        -------
        Image.Image
            Image with the logo composited at the center.
        """
        assert self.center_image_path is not None  # guaranteed by caller

        center_size = int(actual_size * self.logo_size_ratio)
        logo = Image.open(self.center_image_path).resize(
            (center_size, center_size), Image.Resampling.LANCZOS
        )

        if img.mode != "RGBA":
            img = img.convert("RGBA")

        pos = ((actual_size - center_size) // 2, (actual_size - center_size) // 2)

        if logo.mode in ("RGBA", "LA"):
            img.paste(logo, pos, logo)
        else:
            img.paste(logo, pos)

        print(f"Logo placed at {pos}, size {center_size}x{center_size}px")
        return img

    def _save(self, img: Image.Image) -> Path:
        """Save the rendered image to :attr:`filename`.

        Parameters
        ----------
        img : Image.Image
            Final composited image.

        Returns
        -------
        Path
            Path to the saved file.

        Raises
        ------
        ValueError
            If a ``.pdf`` extension is combined with ``transparent_bg=True``.
        """
        if self.filename.suffix.lower() == ".pdf":
            if self.transparent_bg:
                msg = "PDF does not support transparency; use PNG or set transparent_bg=False."
                raise ValueError(msg)
            if img.mode != "RGB":
                img = img.convert("RGB")
            save_format = "PDF"
        else:
            if self.transparent_bg:
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
            else:
                if img.mode != "RGB":
                    img = img.convert("RGB")
            save_format = "PNG"

        if self.size != img.size[0]:
            img = img.resize((self.size, self.size), Image.Resampling.LANCZOS)

        save_kwargs: dict[str, Any] = {"dpi": (300, 300)}
        if save_format == "PNG":
            save_kwargs["optimize"] = True
        img.save(self.filename, save_format, **save_kwargs)

        print(f"Saved: {self.filename}")
        return self.filename
