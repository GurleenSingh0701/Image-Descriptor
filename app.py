import os
import io
import datetime
from dotenv import load_dotenv
import streamlit as st
from google import genai
from google.genai import types
import PIL.Image

import prompts

# ---------------------------------------------------------
# Page Configuration & Custom CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="VisionAI Pro | Image Content Suite",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .badge {
        background-color: #E2E8F0;
        color: #334155;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.4rem;
    }
    .status-ok {
        background-color: #DEF7EC;
        color: #03543F;
    }
    .status-error {
        background-color: #FDE8E8;
        color: #9B1C1C;
    }
    .output-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 8px;
        padding-bottom: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "vqa_chat" not in st.session_state:
    st.session_state.vqa_chat = []

if "generated_outputs" not in st.session_state:
    st.session_state.generated_outputs = {}

# ---------------------------------------------------------
# Sidebar - Configuration & Controls
# ---------------------------------------------------------
with st.sidebar:
    st.title("⚙: Directives & Settings")
    st.markdown("---")

    # API Key loaded silently from environment
    active_api_key = os.getenv('GOOGLE_API_KEY', '')

    # Model Selection
    model_choice = st.selectbox(
        "Gemini Vision Model",
        options=[
            "gemini-2.5-flash",
            "gemini-3.1-flash-lite",
            "gemini-2.5-pro",
        ],
        index=0,
        help="Select model balance between speed and advanced reasoning."
    )

    # Generation Hyperparameters
    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Higher values produce more creative outputs, lower values produce precise descriptions."
    )

    tone = st.selectbox(
        "Content Tone / Style",
        options=["Engaging & Narrative", "Professional & Formal", "Casual & Fun", "Persuasive / Sales", "Poetic & Artistic", "Minimalist & Direct"],
        index=0
    )

    blog_length = st.select_slider(
        "Target Blog Length",
        options=["Short (~300 words)", "Medium (~500 words)", "Detailed (800+ words)"],
        value="Medium (~500 words)"
    )

    st.markdown("---")

    # Clear History Action
    if st.button("🗑️ Clear Session History", width="stretch"):
        st.session_state.history = []
        st.session_state.vqa_chat = []
        st.session_state.generated_outputs = {}
        st.success("Session state cleared!")
        st.rerun()

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def get_genai_client(api_key: str):
    if not api_key:
        st.error("Please provide a valid GOOGLE_API_KEY in `.env` or in the sidebar.")
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing GenAI Client: {e}")
        return None

def generate_vision_response(client, model: str, prompt: str, image: PIL.Image.Image, temperature: float = 0.7) -> str:
    """Invokes Google GenAI API with image content."""
    try:
        config = types.GenerateContentConfig(
            temperature=temperature,
        )
        response = client.models.generate_content(
            model=model,
            contents=[prompt, image],
            config=config
        )
        return response.text if response.text else "No text generated."
    except Exception as e:
        return f"❌ Error generating content: {e}"

def add_to_history(category: str, prompt: str, output: str, image_name: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append({
        "timestamp": timestamp,
        "category": category,
        "image_name": image_name,
        "output": output
    })

# ---------------------------------------------------------
# Main UI Layout
# ---------------------------------------------------------
st.markdown('<div class="main-header">📷 VisionAI Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform any image into rich blog posts, social media captions, SEO metadata, e-commerce listings, and visual Q&A insights.</div>', unsafe_allow_html=True)

# Main Image Uploader
uploaded_file = st.file_uploader(
    "Upload Image (PNG, JPG, JPEG, WEBP)",
    type=["png", "jpg", "jpeg", "webp"],
    key="main_image_uploader"
)

if uploaded_file is not None:
    try:
        image = PIL.Image.open(uploaded_file)
    except Exception as e:
        st.error(f"Could not open image file: {e}")
        st.stop()

    # Top Section: Image Preview & Details
    col_img, col_info = st.columns([1, 2])
    with col_img:
        st.image(image, width="stretch", caption=uploaded_file.name)

    with col_info:
        st.subheader("🖼️ Image Metadata")
        st.markdown(f"**Filename:** `{uploaded_file.name}`")
        st.markdown(f"**Dimensions:** `{image.width} x {image.height} px` (Aspect Ratio: `{image.width/image.height:.2f}`)")
        st.markdown(f"**Format:** `{image.format}` | **Color Mode:** `{image.mode}`")
        st.markdown(f"**File Size:** `{uploaded_file.size / 1024:.1f} KB`")
        
        st.info("💡 Select a feature tab below to generate specialized content from this image.")

    st.markdown("---")

    # Setup GenAI Client
    client = get_genai_client(active_api_key)

    # Content Generation Tabs
    tab_blog, tab_social, tab_seo, tab_ecom, tab_vqa, tab_custom, tab_history = st.tabs([
        "📝 Blog Post",
        "📱 Social Media",
        "🌐 SEO & Alt Text",
        "🛍️ E-Commerce",
        "💬 Visual Q&A",
        "🎨 Custom Studio",
        "📜 History Log"
    ])

    # ---------------------------------------------------------
    # TAB 1: Blog & Narrative
    # ---------------------------------------------------------
    with tab_blog:
        st.subheader("📝 Blog Post & Story Generator")
        st.caption("Generate a full-length, structured blog article based on the image visual details.")

        col_b1, col_b2 = st.columns([3, 1])
        with col_b1:
            st.markdown(f"**Current Configuration:** Tone = `{tone}`, Target Length = `{blog_length}`")
        with col_b2:
            btn_gen_blog = st.button("✨ Generate Blog Post", key="btn_blog", type="primary", width="stretch")

        if btn_gen_blog:
            if client is None:
                st.warning("Please configure your Google API Key in the sidebar.")
            else:
                with st.spinner("Writing engaging blog post..."):
                    prompt = prompts.get_blog_prompt(tone=tone, length=blog_length)
                    output = generate_vision_response(client, model_choice, prompt, image, temperature)
                    st.session_state.generated_outputs["blog"] = output
                    add_to_history("Blog Post", prompt, output, uploaded_file.name)

        if "blog" in st.session_state.generated_outputs:
            st.markdown("### Generated Blog Article")
            st.markdown(st.session_state.generated_outputs["blog"])
            st.download_button(
                "📥 Download Blog (.md)",
                data=st.session_state.generated_outputs["blog"],
                file_name=f"blog_{uploaded_file.name}.md",
                mime="text/markdown"
            )

    # ---------------------------------------------------------
    # TAB 2: Social Media Pack
    # ---------------------------------------------------------
    with tab_social:
        st.subheader("📱 Social Media Copywriter")
        st.caption("Generate Instagram captions + hashtags, LinkedIn posts, and Twitter/X threads.")

        platform_scope = st.radio(
            "Target Platform Focus",
            options=["All Platforms", "Instagram", "LinkedIn", "Twitter / X"],
            horizontal=True
        )

        if st.button("✨ Generate Social Media Content", key="btn_social", type="primary"):
            if client is None:
                st.warning("Please configure your Google API Key in the sidebar.")
            else:
                with st.spinner("Crafting viral social media content..."):
                    prompt = prompts.get_social_media_prompt(platform_filter=platform_scope)
                    output = generate_vision_response(client, model_choice, prompt, image, temperature)
                    st.session_state.generated_outputs["social"] = output
                    add_to_history("Social Media", prompt, output, uploaded_file.name)

        if "social" in st.session_state.generated_outputs:
            st.markdown("### Generated Social Media Pack")
            st.markdown(st.session_state.generated_outputs["social"])
            st.download_button(
                "📥 Download Social Copy (.txt)",
                data=st.session_state.generated_outputs["social"],
                file_name=f"social_{uploaded_file.name}.txt",
                mime="text/plain"
            )

    # ---------------------------------------------------------
    # TAB 3: SEO & Alt Text
    # ---------------------------------------------------------
    with tab_seo:
        st.subheader("🌐 Accessibility & SEO Metadata")
        st.caption("Generate concise ALT text, accessible description, SEO filename, and image keywords.")

        if st.button("✨ Generate SEO & Alt Text", key="btn_seo", type="primary"):
            if client is None:
                st.warning("Please configure your Google API Key in the sidebar.")
            else:
                with st.spinner("Analyzing image accessibility & SEO..."):
                    prompt = prompts.get_seo_accessibility_prompt()
                    output = generate_vision_response(client, model_choice, prompt, image, temperature=0.2)
                    st.session_state.generated_outputs["seo"] = output
                    add_to_history("SEO & Alt Text", prompt, output, uploaded_file.name)

        if "seo" in st.session_state.generated_outputs:
            st.markdown("### SEO & Accessibility Report")
            st.markdown(st.session_state.generated_outputs["seo"])
            st.download_button(
                "📥 Download SEO Report (.md)",
                data=st.session_state.generated_outputs["seo"],
                file_name=f"seo_{uploaded_file.name}.md",
                mime="text/markdown"
            )

    # ---------------------------------------------------------
    # TAB 4: E-Commerce Listing
    # ---------------------------------------------------------
    with tab_ecom:
        st.subheader("🛍️ E-Commerce Product Listing")
        st.caption("Generate product title, tagline, key highlights, description, and tags.")

        if st.button("✨ Generate Product Listing", key="btn_ecom", type="primary"):
            if client is None:
                st.warning("Please configure your Google API Key in the sidebar.")
            else:
                with st.spinner("Analyzing product details..."):
                    prompt = prompts.get_ecommerce_prompt()
                    output = generate_vision_response(client, model_choice, prompt, image, temperature=0.5)
                    st.session_state.generated_outputs["ecom"] = output
                    add_to_history("E-Commerce", prompt, output, uploaded_file.name)

        if "ecom" in st.session_state.generated_outputs:
            st.markdown("### Generated E-Commerce Listing")
            st.markdown(st.session_state.generated_outputs["ecom"])
            st.download_button(
                "📥 Download Listing (.md)",
                data=st.session_state.generated_outputs["ecom"],
                file_name=f"ecommerce_{uploaded_file.name}.md",
                mime="text/markdown"
            )

    # ---------------------------------------------------------
    # TAB 5: Visual Q&A Chat
    # ---------------------------------------------------------
    with tab_vqa:
        st.subheader("💬 Interactive Visual Q&A")
        st.caption("Ask specific questions about objects, text, colors, or details in this image.")

        user_q = st.text_input("Ask a question about this image:", placeholder="e.g. What brand of shoes is visible? What is written on the sign?")
        
        if st.button("🔍 Answer Question", key="btn_vqa", type="primary"):
            if not user_q.strip():
                st.warning("Please enter a question first.")
            elif client is None:
                st.warning("Please configure your Google API Key in the sidebar.")
            else:
                with st.spinner("Examining image details..."):
                    prompt = prompts.get_vqa_prompt(user_q.strip())
                    answer = generate_vision_response(client, model_choice, prompt, image, temperature=0.3)
                    st.session_state.vqa_chat.append({
                        "question": user_q.strip(),
                        "answer": answer
                    })
                    add_to_history("Visual Q&A", prompt, answer, uploaded_file.name)

        if st.session_state.vqa_chat:
            st.markdown("### Conversation History")
            for idx, qa in enumerate(reversed(st.session_state.vqa_chat)):
                st.markdown(f"**Q:** {qa['question']}")
                st.markdown(f"**A:** {qa['answer']}")
                st.markdown("---")

    # ---------------------------------------------------------
    # TAB 6: Custom Studio
    # ---------------------------------------------------------
    with tab_custom:
        st.subheader("🎨 Custom Prompt Studio")
        st.caption("Provide your own specialized prompt instructions to analyze the image.")

        custom_instructions = st.text_area(
            "Custom Instructions",
            height=140,
            placeholder="e.g. Count all the people in the photo and estimate their age group. List all visible background elements."
        )

        if st.button("🚀 Execute Custom Prompt", key="btn_custom", type="primary"):
            if not custom_instructions.strip():
                st.warning("Please enter instructions.")
            elif client is None:
                st.warning("Please configure your Google API Key in the sidebar.")
            else:
                with st.spinner("Processing custom instructions..."):
                    prompt = prompts.get_custom_prompt(custom_instructions.strip(), tone=tone)
                    output = generate_vision_response(client, model_choice, prompt, image, temperature)
                    st.session_state.generated_outputs["custom"] = output
                    add_to_history("Custom Studio", prompt, output, uploaded_file.name)

        if "custom" in st.session_state.generated_outputs:
            st.markdown("### Custom Output")
            st.markdown(st.session_state.generated_outputs["custom"])
            st.download_button(
                "📥 Download Result (.txt)",
                data=st.session_state.generated_outputs["custom"],
                file_name=f"custom_{uploaded_file.name}.txt",
                mime="text/plain"
            )

    # ---------------------------------------------------------
    # TAB 7: History Log
    # ---------------------------------------------------------
    with tab_history:
        st.subheader("📜 Session Activity Log")
        st.caption("Review all content generated during your current session.")

        if not st.session_state.history:
            st.info("No content has been generated yet in this session.")
        else:
            for item in reversed(st.session_state.history):
                with st.expander(f"[{item['timestamp']}] {item['category']} - {item['image_name']}"):
                    st.markdown(item["output"])

else:
    # Empty State
    st.info("👆 Please upload an image using the file uploader above to get started.")
