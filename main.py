import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image
import os

api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def give_prompt(paragraph, headline, appointment, industry, services, audience, parameters,base):
    prompt = f''' You are a professional graphic designer for a {appointment} of {industry} whose primary services are {services}. Your audience is {audience} working professionally in {industry}
                Generate a realistic image based on the following paragraph:{paragraph} and following headline:{headline} 
                This paragraph will be posted along with the image.
                Create the image based on this base visuals:{base}
                These are the image parameters: {parameters}
                Ensure the image is very simple, realistic, and professional, suitable for a LinkedIn. Human subjects are not mandatory
                Don't put too many details and the image must make sense when posted with the paragraph
                Make sure to not include too detailed objects the objects have to to very realistic and the image should be zoomed in on an object'''
    return prompt

def generate_image(caption):
    # Generate the image
    response = client.images.generate(
        model="dall-e-3",
        prompt=caption,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def fetch_and_display_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        st.error("Failed to retrieve the image.")
        return None

def give_image(paragraph, headline, appointment, industry, services, audience, parameters,base):
    prompt = give_prompt(paragraph, headline, appointment, industry, services, audience, parameters,base)
    st.write("Generating Image...")
    image_url = generate_image(prompt)
    st.write(image_url)
    img = fetch_and_display_image(image_url)
    if img:
        st.image(img,caption="Generated Image")
    return image_url

# Streamlit app
# st.title('Image Generator for LinkedIn Posts')

st.set_page_config(page_title="Image Generator for LinkedIn Posts")

paragraph = st.text_area("Paragraph", "")

headline = st.text_input("Headline", "")

appointment = st.text_input("Appointment", "")
industry = st.text_input("Industry", "")
services = st.text_input("Services", "")
audience = st.text_input("Audience", "")
base = st.text_input("Base Prompt", "")

parameters = {
    "vectors": st.text_input("Vectors", ""),
    "photos": st.text_input("Photos", ""),
    "colours": st.text_input("Colours", ""),
    "filetype": st.text_input("Filetype", ""),
    "size": st.text_input("Size", "")
}

if st.button("Generate Image"):
    give_image(paragraph, headline, appointment, industry, services, audience, parameters,base)
