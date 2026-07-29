# 📷 VisionAI Pro - Advanced Image & Content Suite

VisionAI Pro is a high-powered, multi-modal AI vision application built with **Streamlit** and the official **Google GenAI SDK** (`google-genai`). It transforms any uploaded image into rich, professional content across multiple specialized categories.

---

## ✨ Features

- **📝 Blog Post & Narrative Generator**: Generates full-length, structured blog posts with customizable tones (Engaging, Professional, Casual, Poetic) and target lengths (300w, 500w, 800+w).
- **📱 Social Media Copywriter**: Generates tailored social media copy for **Instagram** (captions + hashtags), **LinkedIn** (insights & CTA), **Twitter/X** (thread starters), and **Pinterest/Facebook**.
- **🌐 Accessibility & SEO Engine**: Produces concise ALT text (<125 chars), detailed accessible descriptions, optimized SEO image filenames, and image keyword tags.
- **🛍️ E-Commerce Merchandiser**: Generates product titles, taglines, highlight bullet points, persuasive product descriptions, and target audience profiles.
- **💬 Interactive Visual Q&A**: Real-time visual interrogation allowing users to ask specific questions about objects, text, colors, or details in the uploaded image.
- **🎨 Custom Prompt Studio**: Customizable workspace allowing arbitrary custom prompts and system directives for tailored image analysis.
- **⚙️ Advanced Sidebar Controls**:
  - Gemini Model selection (`gemini-2.5-flash`, `gemini-3.1-flash-lite`, `gemini-2.5-pro`).
  - Temperature / Creativity slider.
  - Flexible API Key configuration (environment variable `.env` or in-app sidebar override).
- **📜 Session History & Export**: One-click download buttons for generated Markdown/TXT content and an interactive session log.

---

## 🛠️ Project Structure

```
Image-Descriptor/
├── app.py              # Main Streamlit application & interactive UI
├── prompts.py          # Modular prompt templates for all generation modes
├── requirements.txt    # Python dependencies
├── .env                # Environment configuration (GOOGLE_API_KEY)
└── README.md           # Documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites & Installation

Ensure Python 3.10+ is installed. Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

*(Alternatively, you can enter your API Key directly in the app's sidebar).*

### 3. Launch Application

Run the Streamlit application:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📄 License

MIT License. Created with Google GenAI & Streamlit.
