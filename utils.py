"""
Image utility helpers — validation, resizing, conversion.
"""
from PIL import Image
import io
from config import MAX_FILE_SIZE_MB, MAX_IMAGE_DIMENSION


def validate_image(uploaded_file) -> tuple[bool, str]:
    """
    Validate the uploaded file size.
    Returns (is_valid, error_message).
    """
    # Check file size
    uploaded_file.seek(0, 2)
    size_mb = uploaded_file.tell() / (1024 * 1024)
    uploaded_file.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large ({size_mb:.1f} MB). Max is {MAX_FILE_SIZE_MB} MB."

    return True, ""


def resize_if_needed(image: Image.Image, max_dim: int = MAX_IMAGE_DIMENSION) -> Image.Image:
    """
    Resize an image so its longest side ≤ max_dim, preserving aspect ratio.
    Returns the (possibly resized) image.
    """
    w, h = image.size
    if max(w, h) <= max_dim:
        return image

    if w >= h:
        new_w = max_dim
        new_h = int(h * (max_dim / w))
    else:
        new_h = max_dim
        new_w = int(w * (max_dim / h))

    return image.resize((new_w, new_h), Image.LANCZOS)


def image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert a PIL Image to raw bytes."""
    buf = io.BytesIO()
    image.save(buf, format=fmt)
    return buf.getvalue()


def bytes_to_image(data: bytes) -> Image.Image:
    """Convert raw bytes back to a PIL Image."""
    return Image.open(io.BytesIO(data))
