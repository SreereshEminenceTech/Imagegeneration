"""
Template system — defines style presets and prompt builder.
"""
from config import FACE_BOOST_SUFFIX, DEFAULT_NEGATIVE_PROMPT

# ─── Template Definitions ────────────────────────────────────
TEMPLATES = {
    "Corporate CEO": {
        "prompt": (
            "professional corporate portrait, formal tailored suit, "
            "modern glass office background, soft studio lighting, "
            "ultra realistic, 8k, sharp focus"
        ),
        "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
        "strength": 0.65,
        "icon": "💼",
    },
    "Cinematic Hero": {
        "prompt": (
            "cinematic portrait, dramatic rim lighting, shallow depth of field, "
            "movie still, film grain, high contrast, anamorphic lens, "
            "dark moody background, ultra detailed"
        ),
        "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
        "strength": 0.70,
        "icon": "🎬",
    },
    "Fantasy Warrior": {
        "prompt": (
            "epic fantasy warrior portrait, ornate magical armor, glowing runes, "
            "enchanted forest background, volumetric fog, golden hour lighting, "
            "ultra detailed, concept art style"
        ),
        "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
        "strength": 0.75,
        "icon": "⚔️",
    },
    "Anime Style": {
        "prompt": (
            "anime portrait, Studio Ghibli inspired, cel shading, vibrant colors, "
            "detailed eyes, clean linework, soft pastel background, "
            "high quality anime art"
        ),
        "negative_prompt": DEFAULT_NEGATIVE_PROMPT + ", photorealistic",
        "strength": 0.80,
        "icon": "🎨",
    },
    "Vintage Film": {
        "prompt": (
            "vintage 1970s film photograph, retro color grading, warm tones, "
            "light leaks, soft grain, nostalgic mood, Kodak Portra 400 style, "
            "analog photography look"
        ),
        "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
        "strength": 0.60,
        "icon": "📷",
    },
}


def get_template_names() -> list[str]:
    """Return all template names."""
    return list(TEMPLATES.keys())


def get_template(name: str) -> dict:
    """Return a single template dict by name."""
    return TEMPLATES[name]


def build_prompt(template_name: str, face_boost: bool = True) -> str:
    """
    Build the final positive prompt for a template.
    Optionally appends the face-preservation suffix.
    """
    tpl = TEMPLATES[template_name]
    prompt = tpl["prompt"]
    if face_boost:
        prompt += FACE_BOOST_SUFFIX
    return prompt
