
import base64
from io import BytesIO
import mimetypes
from pathlib import Path

from PIL import Image

# Project root
BASE_DIR = Path(__file__).resolve().parents[1]


def load_image(image_path):
    """Load an image and return its base64 representation."""

    path = BASE_DIR / image_path

    if not path.is_file():
        return None

    try:
        image_bytes = path.read_bytes()
        with Image.open(BytesIO(image_bytes)) as image:
            image.verify()
    except (OSError, ValueError):
        return None

    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_image}"
