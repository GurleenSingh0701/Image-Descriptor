from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import PIL.Image
import time

load_dotenv()



genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model_img=genai.GenerativeModel('gemini-pro-vision')
st.title("Image Description Generator")

img=st.file_uploader(':blue[Upload an image]',type=['png','jpg','jpeg'],key='image_uploader')

if img is not None:
    image = PIL.Image.open(img)
    st.image(image,width=300,use_column_width=False)

    with st.spinner('Extracting Text from image'):
        time.sleep(1)
        response = model_img.generate_content(["Write a engaging blog post based on this picture of minimum 500 words. It should include a description of the photo", image])
        response.resolve()
        st.header('Generated Text')
        st.write(
           response.text)
           








