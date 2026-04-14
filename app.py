"""
AI Image Transformation POC 🚀
Main Streamlit application — upload, transform, compare.
"""
import streamlit as st
from PIL import Image
import io
import time

from config import GEMINI_API_KEY, DEFAULT_STRENGTH
from templates import get_template_names, get_template, build_prompt, TEMPLATES
from utils import validate_image, resize_if_needed, image_to_bytes
from api_client import transform_image

# ─── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Image Transformation POC",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ─────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hero Header ────────────────────────────────── */
    .hero-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, transparent 60%);
        animation: pulse-glow 4s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .hero-header h1 {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        position: relative;
        z-index: 1;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-header p {
        color: #a5b4fc;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }

    /* ── Cards ───────────────────────────────────────── */
    .image-card {
        background: linear-gradient(145deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 1.2rem;
        transition: all 0.3s ease;
    }
    .image-card:hover {
        border-color: rgba(139, 92, 246, 0.6);
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2);
    }
    .card-label {
        color: #c4b5fd;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.8rem;
    }

    /* ── Template Card ──────────────────────────────── */
    .template-preview {
        background: linear-gradient(145deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0;
    }
    .template-preview h4 {
        color: #e0e7ff;
        margin: 0 0 0.4rem 0;
    }
    .template-preview p {
        color: #818cf8;
        font-size: 0.85rem;
        margin: 0;
        line-height: 1.5;
    }

    /* ── Generate Button ────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6) !important;
    }

    /* ── Sidebar ────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1e1b4b 100%);
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #c4b5fd !important;
    }

    /* ── Success / Result Badge ─────────────────────── */
    .result-badge {
        background: linear-gradient(135deg, #059669, #10b981);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 8px;
        display: inline-block;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }

    /* ── Divider ────────────────────────────────────── */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #7c3aed, #3b82f6, transparent);
        border: none;
        margin: 1.5rem 0;
    }

    /* ── Hide default header/footer ─────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Hero Header ──────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>AI Image Transformation POC 🚀</h1>
    <p>Upload a photo • Choose a style • Get transformed with AI</p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎨 Style Settings")
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Template selector
    template_names = get_template_names()
    display_names = [f"{TEMPLATES[n]['icon']}  {n}" for n in template_names]
    selected_display = st.selectbox("Choose a Style Template", display_names)
    selected_template = template_names[display_names.index(selected_display)]
    tpl = get_template(selected_template)

    # Template preview
    st.markdown(f"""
    <div class="template-preview">
        <h4>{tpl['icon']}  {selected_template}</h4>
        <p>{tpl['prompt'][:120]}…</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Strength slider
    strength = st.slider(
        "🔧 Transformation Strength",
        min_value=0.3,
        max_value=0.95,
        value=tpl.get("strength", DEFAULT_STRENGTH),
        step=0.05,
        help="Lower = more original face · Higher = more stylized",
    )

    # Face boost toggle
    face_boost = st.checkbox("🛡️ Face Preservation Boost", value=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Strength guide
    st.markdown("""
    **Strength Guide:**
    - `0.3` → Subtle — keeps original face
    - `0.6` → Balanced — recommended ✅
    - `0.9` → Dramatic — heavy stylization
    """)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color: #6366f1; font-size: 0.8rem; margin-top: 1rem;">
        Powered by Gemini AI ✨
    </div>
    """, unsafe_allow_html=True)

# ─── API Key Check ────────────────────────────────────────────
if not GEMINI_API_KEY:
    st.error(
        "⚠️ **API key not found.** "
        "Please add `GEMINI_API_KEY` to your `.env` file."
    )
    st.stop()

# ─── Main Content ─────────────────────────────────────────────
col_upload, col_spacer, col_info = st.columns([3, 0.2, 1.5])

with col_upload:
    st.markdown("### 📤 Upload Your Photo")
    uploaded_file = st.file_uploader(
        "Drag and drop or browse",
        type=["png", "jpg", "jpeg"],
        help="Max 10 MB · PNG, JPG, or JPEG",
        label_visibility="collapsed",
    )

with col_info:
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    1. **Upload** a portrait photo
    2. **Select** a style from the sidebar
    3. **Adjust** transformation strength
    4. **Click** ✨ Generate
    5. **Compare** before & after
    6. **Download** your result
    """)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# ─── Process Image ────────────────────────────────────────────
if uploaded_file:
    # Validate
    is_valid, error_msg = validate_image(uploaded_file)
    if not is_valid:
        st.error(f"❌ {error_msg}")
        st.stop()

    # Load & resize
    input_image = Image.open(uploaded_file).convert("RGB")
    input_image = resize_if_needed(input_image)

    # Show preview
    st.markdown("### 🖼️ Your Photo")
    st.image(input_image, caption="Uploaded Image", use_column_width=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # Generate button
    col_btn_l, col_btn_c, col_btn_r = st.columns([1, 2, 1])
    with col_btn_c:
        generate_clicked = st.button("✨  Generate Transformation")

    if generate_clicked:
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        # Build prompt
        prompt = build_prompt(selected_template, face_boost=face_boost)
        negative = tpl.get("negative_prompt", "")

        # Progress
        progress_bar = st.progress(0, text="Preparing image…")
        time.sleep(0.3)
        progress_bar.progress(20, text="Sending to AI…")

        with st.spinner("🧠 Gemini is transforming your image…"):
            progress_bar.progress(40, text="Processing with AI…")
            result_image = transform_image(
                image=input_image,
                prompt=prompt,
                negative_prompt=negative,
                strength=strength,
            )
            progress_bar.progress(90, text="Almost done…")

        progress_bar.progress(100, text="Complete! ✅")
        time.sleep(0.3)
        progress_bar.empty()

        if result_image:
            st.markdown('<span class="result-badge">✅ Transformation Complete!</span>', unsafe_allow_html=True)
            st.markdown("### 🔄 Before & After")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                <div class="image-card">
                    <div class="card-label">📷 Original</div>
                </div>
                """, unsafe_allow_html=True)
                st.image(input_image, caption="Before", use_column_width=True)

            with col2:
                st.markdown("""
                <div class="image-card">
                    <div class="card-label">✨ Transformed</div>
                </div>
                """, unsafe_allow_html=True)
                st.image(result_image, caption=f"After — {selected_template}", use_column_width=True)

            st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

            # Download button
            result_bytes = image_to_bytes(result_image)
            col_dl_l, col_dl_c, col_dl_r = st.columns([1, 2, 1])
            with col_dl_c:
                st.download_button(
                    label="⬇️  Download Transformed Image",
                    data=result_bytes,
                    file_name=f"transformed_{selected_template.lower().replace(' ', '_')}.png",
                    mime="image/png",
                )

            # Try image comparison slider
            try:
                from streamlit_image_comparison import image_comparison
                st.markdown("### 🔍 Interactive Comparison")
                image_comparison(
                    img1=input_image,
                    img2=result_image,
                    label1="Original",
                    label2=f"Transformed ({selected_template})",
                )
            except ImportError:
                pass  # streamlit-image-comparison not installed, skip

        else:
            st.error(
                "❌ **Transformation failed.** The API didn't return an image. "
                "Please check your API key and try again."
            )

else:
    # Empty state
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; color: #6366f1;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📸</div>
        <h3 style="color: #a5b4fc;">Upload a photo to get started</h3>
        <p style="color: #818cf8;">Your AI transformation is one click away</p>
    </div>
    """, unsafe_allow_html=True)
