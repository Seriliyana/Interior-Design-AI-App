import os
import streamlit as st
from openai import OpenAI

# Access your API key directly from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Function to generate the interior design based on user inputs
def interior_design_ai(place, room, color):
    description = st.text_input("What do you want to design? (Short description)")

    if place == "House":
        room_options = ["Bedroom", "Living Room", "Kitchen", "Toilet", "Powder Room", "Yard", "Balcony"]
    elif place == "Office":
        room_options = ["Pantry", "Office Room", "Meeting Room", "Toilet"]
    elif place == "Shop":
        room_options = ["Dining Area", "Cooking Area", "Counter Area", "Shop Entrance", "Toilet"]
    elif place == "Hotel":
        room_options = ["Guest Rooms and Suites", "Lobby and Reception", "Restaurants and Dining", "Bars and Lounges", "Conference and Event Spaces", "Spa and Wellness Centers", "Fitness Centers and Recreational Spaces", "Hallways, Elevators, and Public Restrooms"]
    else:
        room_options = []  # Add more options based on other places

    selected_room = st.selectbox("Select the room:", room_options)

    # Function to suggest suitable themes for the chosen place
    def suggest_themes(place):
        if place == "House":
            return ["Modern", "Vintage", "Minimalist", "Rustic", "Scandinavian"]
        elif place == "Office":
            return ["Professional", "Contemporary", "Minimalist", "Innovative"]
        elif place == "Shop":
            return ["Elegant", "Cozy", "Industrial", "Chic"]
        elif place == "Hotel":
            return ["Luxurious", "Modern", "Classic", "Resort-style"]
        else:
            return []  # Add more themes for other places

    if st.button("Suggest Suitable Themes"):
        themes = suggest_themes(place)
        st.write(f"Suggested themes for {place}: {themes}")

    if description and room and color:
        user_prompt = f"I want to design a {place.lower()} {selected_room.lower()} with {color} theme. {description}"

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
    prompt=msg,
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


def interior_design_ai(place, room, color):
    description = st.text_input("What do you want to design? (Short description)")
    
    user_prompt = f"I want to design a {place.lower()} {room.lower()} with {color} theme. {description}"
    
    idesign = user_ai(user_prompt)  # Adjust user_ai function to handle user_prompt
    design = design_ai(idesign)
    image = cover_ai(design)

    st.image(image, caption="Generated Image")  # Display the generated image
    st.write("Design Prompt:", design)  # Display the design prompt

# Streamlit app UI
st.title("Interior Design Prompt Generator")

# Input fields for user to specify place, room, and color
place = st.selectbox("What is your place?", ["House", "Office", "Shop", "Hotel"])  # Add more places as needed
color = st.text_input("Enter the desired color:")
room = st.text_input("Enter the room size:")

interior_design_ai(place, room, color)
