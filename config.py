"""
Configuration module — loads environment variables and defines app constants.
"""
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# ─── API Config ───────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ─── App Constants ────────────────────────────────────────────
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
DEFAULT_STRENGTH = 0.65          # 0.0 = keep original, 1.0 = fully stylized
MAX_IMAGE_DIMENSION = 1024       # resize large uploads before sending

# ─── Prompt Suffixes ──────────────────────────────────────────
FACE_BOOST_SUFFIX = (
    ", preserve facial identity, same face, realistic skin texture, "
    "detailed facial features, natural proportions"
)
DEFAULT_NEGATIVE_PROMPT = (
    "blurry, distorted face, extra limbs, bad anatomy, "
    "deformed, disfigured, low quality, watermark, text"
)
