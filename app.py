import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
import os
import requests
import datetime

# API Keys
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAXehSIPZDaWAbFE8xavz-rrEO-rPXPKAw'  
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")
UNSPLASH_ACCESS_KEY = "U22YDJh7jbaVAVHLu_awTDD_PPP74drYbz8WUjjIjXg"

st.title('🌍 Explore the World with AI: Your Travel Companion')

st.subheader('🛫 Plan Your Journey')
origin_country = st.text_input('🌎 Enter your departure location:')
destination_country = st.text_input('🗺️ Enter your travel destination:')

# Calendar-based Date Input
date_from = st.date_input("📅 Departure Date", min_value=datetime.date.today())
date_to = st.date_input("📅 Return Date", min_value=date_from, value=None)

# Compute travel duration only if date_to is selected
num_days = (date_to - date_from).days + 1 if date_to is not None else None

# Manual budget input
budget = st.text_input('💰 Enter Your Budget (₹)', value="")

travel_preferences = st.text_area('🎭 Describe your travel style (e.g., adventure, relaxation, culture, budget-friendly)')

def get_unsplash_image(destination):
    url = f"https://api.unsplash.com/photos/random?query={destination}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url).json()
    return response.get("urls", {}).get("regular", "")

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

def get_packing_suggestions(destination, season, travel_preferences):
    """Generate a packing list using Gemini AI based on the destination and season."""
    packing_prompt = f"""
    I am traveling to {destination} during the {season} season. My travel preferences include {travel_preferences}. 
    Suggest a list of essential items I should pack, including clothing, accessories, and other necessary supplies.
    """
    response = llm.invoke([HumanMessage(content=packing_prompt)])
    return response.split("\n") if response else ["No suggestions available."]


if st.button('🚀 Generate My Travel Plan'):
    if origin_country and destination_country and date_to and budget.isdigit():
        travel_month = date_from.month
        travel_season = get_season(travel_month)

        # Fetch packing suggestions from Gemini AI
        packing_list = get_packing_suggestions(destination_country, travel_season, travel_preferences)

        user_input = f"I am traveling from {origin_country} to {destination_country} from {date_from} to {date_to} ({num_days} days) with a budget of {budget}. I prefer {travel_preferences}. Provide a detailed itinerary."
        messages = [
            SystemMessage(content="You are a professional travel planner AI. Generate a comprehensive travel itinerary including transportation, accommodations, and must-visit attractions."),
            HumanMessage(content=user_input)
        ]
        response = llm.invoke(messages)

        st.subheader('🗺️ Your Personalized Travel Plan:')
        st.write(response)

        st.subheader(f'📅 Season: {travel_season}')
        st.write('👕 **Packing List:**')
        for item in packing_list:
            st.write(f"- {item}")

        unsplash_image_url = get_unsplash_image(destination_country)
        if unsplash_image_url:
            st.image(unsplash_image_url, caption=f"{destination_country} Travel Image", use_column_width=True)

        # Generate downloadable travel plan
        itinerary_text = f"""
        🌍 **Travel Itinerary**  
        - **From:** {origin_country}  
        - **To:** {destination_country}  
        - **Dates:** {date_from} to {date_to} ({num_days} days)  
        - **Budget:** ₹{budget}  
        - **Travel Style:** {travel_preferences}  

        🗺️ **Personalized Travel Plan:**  
        {response}  

        📅 **Season:** {travel_season}  
        🎒 **Packing List:**  
        {', '.join(packing_list)}
        """

        st.download_button(label="📥 Download Travel Plan", data=itinerary_text, file_name="Travel_Plan.txt", mime="text/plain")

    else:
        st.warning('⚠️ Please fill in all the required details correctly.')
