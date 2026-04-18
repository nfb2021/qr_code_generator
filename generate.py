"""Example QR code generation script. Edit and run with: uv run generate.py"""

from qr_code_generator import QRGenerator

# LinkedIn — solid #e1e6b9
QRGenerator(
    data="https://www.linkedin.com/in/nicbad/",
    filename="output/linkedin_solid.pdf",
    size=1400,
    qr_color="#e1e6b9",
    center_image_path="assets/linkedin_logo.png",
    dot_size_ratio=0.9,
    transparent_bg=False,
).generate()

# LinkedIn — mixed #e1e6b9 / #375d3b
QRGenerator(
    data="https://www.linkedin.com/in/nicbad/",
    filename="output/linkedin_mixed.png",
    size=1400,
    qr_color="#e1e6b9",
    qr_color2="#375d3b",
    center_image_path="assets/linkedin_logo.png",
    dot_size_ratio=0.9,
    transparent_bg=True,
).generate()

# GitHub repo
QRGenerator(
    data="https://github.com/nfb2021/qr_code_generator",
    filename="assets/github_repo.png",
    size=1400,
    qr_color="#e1e6b9",
    qr_color2="#375d3b",
    center_image_path="assets/github_icon_white.png",
    logo_size_ratio=0.25,
    dot_size_ratio=0.9,
    transparent_bg=True,
).generate()
