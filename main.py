import qrcode
from PIL import Image, ImageDraw
import os
import random


def create_custom_qr(
        data,
        filename="custom_qr.pdf",
        size=1200,  # Increased default size
        qr_color="#000000",
        qr_color2=None,  # Second color for random selection
        bg_color="#FFFFFF",
        center_image_path=None,
        dot_size_ratio=0.8,
        border_modules=4,
        transparent_bg=False,
        random_seed=None):
    """
    Generate a high-resolution custom QR code with dots instead of squares.

    Args:
        data (str): Text or URL to encode
        filename (str): Output filename
        size (int): Size of the QR code image in pixels (recommended: 800+)
        qr_color (str): Primary hex color code for QR dots
        qr_color2 (str): Secondary hex color code for random variation (optional)
        bg_color (str): Hex color code for background (ignored if transparent_bg=True)
        center_image_path (str): Path to center image (optional)
        dot_size_ratio (float): Size of dots relative to module size (0.1-1.0)
        border_modules (int): Number of border modules around QR code
        transparent_bg (bool): Make background transparent (PNG format required)
        random_seed (int): Seed for random color selection (for reproducible results)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Set random seed if provided for reproducible results
        if random_seed is not None:
            random.seed(random_seed)

        # Determine if we're using random colors
        use_random_colors = qr_color2 is not None
        color_options = [qr_color, qr_color2
                         ] if use_random_colors else [qr_color]

        # Create QR code with optimal settings for high resolution
        qr = qrcode.QRCode(
            version=None,  # Let it auto-determine the best version
            error_correction=qrcode.constants.
            ERROR_CORRECT_H,  # Highest error correction - FIXED SYNTAX
            box_size=1,  # We'll handle scaling manually for better quality
            border=border_modules,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Get the QR matrix
        qr_matrix = qr.get_matrix()

        # Calculate dimensions for high resolution
        module_count = len(qr_matrix)

        # Ensure we have enough pixels per module for smooth circles
        min_module_size = 8  # Minimum pixels per module for good quality
        calculated_module_size = max(size // module_count, min_module_size)

        # Recalculate actual image size based on module size
        actual_size = calculated_module_size * module_count

        print(f"Generating QR code: {module_count}x{module_count} modules")
        print(f"Module size: {calculated_module_size}px")
        print(f"Final image size: {actual_size}x{actual_size}px")

        # Create high-resolution image with proper color mode
        if transparent_bg:
            img = Image.new('RGBA', (actual_size, actual_size),
                            (0, 0, 0, 0))  # Transparent
        else:
            img = Image.new('RGB', (actual_size, actual_size), bg_color)

        draw = ImageDraw.Draw(img)

        # Calculate dot radius for smooth circles
        dot_radius = (calculated_module_size * dot_size_ratio) / 2

        # Draw dots with random colors if specified
        for i in range(module_count):
            for j in range(module_count):
                if qr_matrix[i][j]:
                    # Calculate center of the module
                    center_x = j * calculated_module_size + calculated_module_size // 2
                    center_y = i * calculated_module_size + calculated_module_size // 2

                    # Choose color (random if two colors provided)
                    dot_color = random.choice(
                        color_options) if use_random_colors else qr_color

                    # Draw main dot
                    draw.ellipse([
                        center_x - dot_radius, center_y - dot_radius,
                        center_x + dot_radius, center_y + dot_radius
                    ],
                                 fill=dot_color)

        # Add center image if provided - CLEAN INTEGRATION
        if center_image_path and os.path.exists(center_image_path):
            try:
                print(f"Adding center image: {center_image_path}")
                center_img = Image.open(center_image_path)

                # Calculate center image size (about 1/6 of QR code - smaller but cleaner)
                center_size = actual_size // 6
                print(f"Center image size: {center_size}x{center_size}px")

                # Resize center image with high-quality resampling
                center_img = center_img.resize((center_size, center_size),
                                               Image.Resampling.LANCZOS)

                # Convert main image to RGBA for proper blending
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Calculate position to center the logo on QR code
                pos_x = (actual_size - center_size) // 2
                pos_y = (actual_size - center_size) // 2

                print(f"Placing center image at position: ({pos_x}, {pos_y})")

                # Handle logo with transparency - paste directly without extra background
                if center_img.mode in ('RGBA', 'LA'):
                    img.paste(center_img, (pos_x, pos_y), center_img)
                else:
                    center_img_rgba = center_img.convert('RGBA')
                    img.paste(center_img_rgba, (pos_x, pos_y))

                print("Center image successfully added")

            except Exception as e:
                print(f"Warning: Could not add center image: {e}")
                import traceback
                traceback.print_exc()

        # Determine output format from filename extension
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            if transparent_bg:
                raise ValueError("PDF does not support transparency; set transparent_bg=False or use PNG.")
            if img.mode != 'RGB':
                img = img.convert('RGB')
            save_format = "PDF"
        else:
            if transparent_bg:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
            else:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
            save_format = "PNG"

        # If the requested size is different from actual size, resize with high quality
        if size != actual_size:
            img = img.resize((size, size), Image.Resampling.LANCZOS)

        # Save with high quality
        save_kwargs = {"dpi": (300, 300)}
        if save_format == "PNG":
            save_kwargs["optimize"] = True
        img.save(filename, save_format, **save_kwargs)

        bg_type = "transparent" if transparent_bg else f"solid ({bg_color})"
        color_info = f"random colors ({qr_color}, {qr_color2})" if use_random_colors else f"single color ({qr_color})"
        print(
            f"High-resolution QR code saved as {filename} with {bg_type} background using {color_info}"
        )
        return True

    except Exception as e:
        print(f"Error generating QR code: {e}")
        import traceback
        traceback.print_exc()
        return False



if __name__ == "__main__":

    # LinkedIn — solid #e1e6b9
    create_custom_qr(
        data="https://www.linkedin.com/in/nicbad/",
        filename="output/linkedin_solid.pdf",
        size=1400,
        qr_color="#e1e6b9",
        center_image_path="assets/linkedin_logo.png",
        dot_size_ratio=0.9,
        transparent_bg=False)

    # LinkedIn — mixed #e1e6b9 / #375d3b
    create_custom_qr(
        data="https://www.linkedin.com/in/nicbad/",
        filename="output/linkedin_mixed.png",
        size=1400,
        qr_color="#e1e6b9",
        qr_color2="#375d3b",
        center_image_path="assets/linkedin_logo.png",
        dot_size_ratio=0.9,
        transparent_bg=True)
