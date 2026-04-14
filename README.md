# AI Image Transformation POC 🚀

Transform photos into stunning AI-styled portraits using Google Gemini.

## Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 3. Run the app
streamlit run app.py
```

## Features

- 📤 **Upload** any portrait photo (PNG/JPG, up to 10 MB)
- 🎨 **5 Style Templates** — Corporate CEO, Cinematic Hero, Fantasy Warrior, Anime, Vintage Film
- 🔧 **Strength Control** — fine-tune how much transformation to apply
- 🛡️ **Face Preservation** — keeps facial identity intact
- 🔄 **Before/After** — side-by-side + interactive slider comparison
- ⬇️ **Download** — save your transformed image

## 🚀 Production Deployment (Streamlit Community Cloud)

This app is production-ready for **Streamlit Community Cloud** (which is 100% free).

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**.
3. Select your repository `Imagegeneration`, branch `main`, and main file path `app.py`.
4. Click **Advanced settings** before deploying!
5. In the Secrets text box, paste your API key exactly like this:
   ```toml
   GEMINI_API_KEY = "your_actual_paid_api_key_here"
   ```
6. Click Save and then **Deploy!** 

## Project Structure

```
├── app.py              # Streamlit UI
├── config.py           # Config & env loading
├── templates.py        # Style template definitions
├── api_client.py       # Gemini API integration
├── utils.py            # Image helpers
├── requirements.txt    # Dependencies
└── .env                # API keys (not committed)
```

## Style Templates

| Template | Strength | Description |
|----------|----------|-------------|
| 💼 Corporate CEO | 0.65 | Professional office portrait |
| 🎬 Cinematic Hero | 0.70 | Movie-still dramatic lighting |
| ⚔️ Fantasy Warrior | 0.75 | Epic fantasy armor & magic |
| 🎨 Anime Style | 0.80 | Studio Ghibli-inspired art |
| 📷 Vintage Film | 0.60 | Retro 70s Kodak film look |

## Strength Guide

- **0.3** → Subtle — preserves most of the original
- **0.6** → Balanced — recommended for most use cases
- **0.9** → Dramatic — heavy stylisation

---

*Powered by Google Gemini AI ✨*
