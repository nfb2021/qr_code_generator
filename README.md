# QR Code Generator

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

Edit the `__main__` block in `main.py` and run:

```bash
uv run main.py
```

Output files are saved to the `output/` directory.

## API

```python
from main import create_custom_qr

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
| `dot_size_ratio` | `0.8` | Dot size relative to module (0.1–1.0) |
| `border_modules` | `4` | Quiet zone width in modules |
| `transparent_bg` | `False` | Transparent background (PNG only) |
| `random_seed` | `None` | Seed for reproducible color randomness |
