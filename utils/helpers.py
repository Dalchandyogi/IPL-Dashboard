
import base64
import mimetypes
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[1]


def load_image(image_path):
    """Load an image and return its base64 representation."""

    path = BASE_DIR / image_path

    if not path.exists():
        return None

    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded_image = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_image}"
