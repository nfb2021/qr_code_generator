# QR Code Generator

[![GitHub](assets/github_icon_dark.webp)](https://github.com/nfb2021/qr_code_generator)

Generate high-resolution custom QR codes with circular dot styling and optional center logos.

## Features

- Circular/dot-style QR modules instead of squares
- Optional center logo overlay
- Transparent background support
- Two-color random dot variation
- High-resolution output (300 DPI)

## Setup

```bash
uv sync
```

## Usage

Edit `generate.py` and run:

```bash
uv run generate.py
```

Output files are saved to the `output/` directory.

## API

```python
from qr_code_generator import create_custom_qr

create_custom_qr(
    data="https://example.com",
    filename="output/my_qr.png",
    size=1400,
    qr_color="#12384F",
    qr_color2="#1D5041",   # optional: enables random two-color dots
    center_image_path="logo.png",
    dot_size_ratio=0.9,    # 0.1–1.0
    transparent_bg=True,
    random_seed=42,        # optional: reproducible random colors
)
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `data` | — | URL or text to encode |
| `filename` | `"custom_qr.pdf"` | Output file path |
| `size` | `1200` | Image size in pixels |
| `qr_color` | `"#000000"` | Primary dot color |
| `qr_color2` | `None` | Secondary color for random variation |
| `bg_color` | `"#FFFFFF"` | Background color (ignored if transparent) |
| `center_image_path` | `None` | Path to center logo (PNG/PDF) |
| `logo_size_ratio` | `1/6` | Logo size as a fraction of the QR image size (e.g. `0.2` = 20%) |
| `dot_size_ratio` | `0.8` | Dot size relative to module (0.1–1.0) |
| `border_modules` | `4` | Quiet zone width in modules |
| `transparent_bg` | `False` | Transparent background (PNG only) |
| `random_seed` | `None` | Seed for reproducible color randomness |

### Adding logos

Logo files in `assets/` are gitignored by default. To track a new logo, add an explicit exception to `.gitignore`:

```
!assets/your_logo.png
```

Without this, the logo will not be committed and the QR generation will fail for anyone else cloning the repo.

### Output formats

The format is inferred from the `filename` extension:

- **PNG** — supports transparency (`transparent_bg=True`). Use this for overlaying the QR on other designs.
- **PDF** — does **not** support transparency. `transparent_bg` must be `False`; the background will be filled with `bg_color`.
