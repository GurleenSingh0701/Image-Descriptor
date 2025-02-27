from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import PIL.Image
import time

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Use the latest supported vision model. You may need to update this based on current documentation.
# Check the official Google AI documentation for the most up-to-date model name.
try:
    available_models = genai.ListModels()
    st.write("Available Models:")
    for model in available_models:
        st.write(f"- {model.name}: {model.description}")

    # Replace with the CORRECT model name from the list!
    model_img = genai.GenerativeModel('YOUR_CORRECT_MODEL_NAME') # replace this line.

except Exception as e:
    st.error(f"Error initializing model or listing models: {e}. Please ensure you have the correct model name and API key, and that vision models are available to you.")
    st.stop()

st.title("Image Description Generator")

img = st.file_uploader(':blue[Upload an image]', type=['png', 'jpg', 'jpeg'], key='image_uploader')

if img is not None:
    image = PIL.Image.open(img)
    st.image(image, width=300, use_container_width=False) #Replaced use_column_width with use_container_width

    with st.spinner('Extracting Text from image'):
        time.sleep(1)
        prompt = """
        Write an engaging blog post based on this picture, aiming for a minimum of 500 words. 
        It should include a detailed description of the photo, incorporating sensory details and emotional context. 
        Focus on creating a narrative that captures the essence of the image and connects with the reader.
        """
        try:
            response = model_img.generate_content([prompt, image])
            response.resolve()
            st.header('Generated Text')
            st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred during text generation: {e}")
