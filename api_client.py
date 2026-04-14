import base64
import io
import traceback
from PIL import Image
from google import genai
from google.genai import types
from config import GEMINI_API_KEY


def get_client() -> genai.Client:
    """Create and return a Gemini API client."""
    return genai.Client(api_key=GEMINI_API_KEY)


def transform_image(
    image: Image.Image,
    prompt: str,
    negative_prompt: str = "",
    strength: float = 0.65,
) -> Image.Image | None:
    """
    Send an image + prompt to Gemini for AI transformation.

    Args:
        image: PIL Image to transform.
        prompt: The style/transformation prompt.
        negative_prompt: Things to avoid (appended to prompt).
        strength: Controls how much to transform (0.0–1.0).

    Returns:
        Transformed PIL Image, or None on failure.
    """
    try:
        client = get_client()

        # Build the full prompt with transformation instructions
        full_prompt = (
            f"Transform this person's photo into the following style while keeping their face and identity intact. "
            f"Style: {prompt}. "
            f"Apply the transformation at intensity level {strength:.0%}. "
        )
        if negative_prompt:
            full_prompt += f"Avoid: {negative_prompt}. "

        full_prompt += (
            "Keep the person's facial features, face shape, and identity clearly recognizable. "
            "The result should be a single high-quality portrait image."
        )

        # Convert PIL Image to bytes for the API
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Call Gemini with image editing
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[
                types.Content(
                    parts=[
                        types.Part.from_bytes(
                            data=img_bytes.read(),
                            mime_type="image/png",
                        ),
                        types.Part.from_text(text=full_prompt),
                    ]
                )
            ]
        )

        # Extract image from response
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    img_data = part.inline_data.data
                    return Image.open(io.BytesIO(img_data))

        print("No image found in API response.")
        return None

    except Exception as e:
        print(f"API Error: {e}")
        traceback.print_exc()
        return None
