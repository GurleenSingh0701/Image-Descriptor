"""
Prompt templates and generators for the Advanced Image Descriptor & Content Suite.
"""

def get_blog_prompt(tone: str = "Engaging", length: str = "Medium (500 words)") -> str:
    return f"""
You are an expert content writer and storyteller.
Write a blog post based on the uploaded image.

Configuration:
- Tone: {tone}
- Desired Length: {length}

Instructions:
1. Craft a captivating headline for the blog post.
2. Provide a vivid description of the visual scene incorporating sensory details, mood, and emotional context.
3. Build a compelling narrative around the subject in the photo.
4. Format the output with clean Markdown headers, subheadings, and bullet points where appropriate.
"""


def get_social_media_prompt(platform_filter: str = "All Platforms") -> str:
    return f"""
You are a social media strategist and expert copywriter.
Analyze the image and generate optimized social media content.

Platform Scope: {platform_filter}

Provide content tailored for:
1. **Instagram**: An engaging caption with emojis, a strong hook, call-to-action (CTA), and 15-20 relevant hashtags grouped logically.
2. **LinkedIn**: A professional post drawing key lessons, insights, or industry context from the image, ending with a thought-provoking question.
3. **Twitter / X**: A punchy, viral thread (3-4 tweets) summarizing the scene or story behind the image.
4. **Pinterest / Facebook**: A short, catchy description with key search terms.

Format with clear section titles for easy copying.
"""


def get_seo_accessibility_prompt() -> str:
    return """
You are a web accessibility specialist and SEO expert.
Analyze the uploaded image and provide concise, standard accessibility and SEO metadata.

Structure your response into the following clear sections:
1. **Short Alt Text (Under 125 chars)**: Perfect for `alt=""` attributes.
2. **Detailed Alt Text / Long Description**: Accessible description for visually impaired users explaining layout, colors, text present, and primary subjects.
3. **SEO Image Title & Filename Suggestion**: Optimized, hyphen-separated filenames (e.g. `modern-minimalist-office-desk.jpg`).
4. **SEO Keywords & Image Tags**: A comma-separated list of 15 relevant primary and secondary keywords for image search indexers.
"""


def get_ecommerce_prompt() -> str:
    return """
You are a senior e-commerce merchandising copywriter.
Analyze the product or item shown in the image and write a high-converting e-commerce product listing.

Output Structure:
1. **Catchy Product Title**: Optimized for storefronts and marketplaces.
2. **Short Catchphrase / Tagline**: 1 line value proposition.
3. **Product Highlights (Bullet Points)**: 4-6 key visible features and benefits.
4. **Detailed Description**: A persuasive 2-paragraph product overview.
5. **Target Audience & Best Use Cases**: Who this product is for and how/when to use it.
6. **Estimated Tags/Category**: E-commerce categories and tags.
"""


def get_vqa_prompt(question: str) -> str:
    return f"""
You are a visual intelligence assistant.
Analyze the image carefully and answer the user's specific question.

User Question: {question}

Provide a direct, accurate, and detailed answer based strictly on visual evidence in the image. If something is uncertain or not clearly visible, mention that clearly.
"""


def get_custom_prompt(user_instructions: str, tone: str = "Balanced") -> str:
    return f"""
Analyze the image according to the following custom instructions:

Tone/Style: {tone}
Instructions:
{user_instructions}
"""
