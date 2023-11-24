import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from IPython.display import Image

load_dotenv()

#client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
 api_key = st.secrets["OPENAI_API_KEY"]

 client = OpenAI(api_key=api_key)

# take the description of the user and generate a relevant role for the system message
def user_ai(msg):
    system_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """ You are a best interior designer. You'll suggest the user which design and decoration are suitable with their theme and place. You will also tell them what is the best brand and place that they can purchase the item. please make it in 100 words and converse in a professional way as an interior designer. """
            },
            {
                "role": "user",
                "content": f'{msg}'
            }

        ],
        max_tokens=500,
        temperature=1.3
    )

    role = system_response.choices[0].message.content
    # print(role)
    return role

def cover_ai(msg):
    cover_response = client.images.generate(
    model="dall-e-3",
    prompt=f"{msg} in modern aesthetic brown theme",
    size="1024x1024",
    quality="standard",
    n=1,
    )
    image_url = cover_response.data[0].url
    #print(image_url)
    #display(Image(url=image_url))
    return image_url

# take the story generated and design a relevant prompt for the cover image
def design_ai(msg):
    design_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You will generate a detailed image prompt to design a place that the user requests. The image prompt should follow the theme, color, suitable furniture, and accessories. Can list the recommendation where to buy all the furniture and accessories and what is the best brand."""
            },
            {
                "role": "user",
                "content": f'{msg}'
            }

        ],
        max_tokens=100,
        temperature=1.3
    )

    design_prompt = design_response.choices[0].message.content
    # print(design_prompt)
    return design_prompt


# main function to chain everything
def interior_design_ai(user_prompt):
    idesign = user_ai(user_prompt)
    design = design_ai(idesign)
    image = cover_ai(design)

    st.image(image, caption="Generated Image")  # Display the generated image
    st.write("Design Prompt:", design)  # Display the design prompt


# Example usage
user_prompt = "I have a master bedroom with 200 square feet. I want an aesthetic brown color theme for my room and modern decoration."
interior_design_ai(user_prompt)
