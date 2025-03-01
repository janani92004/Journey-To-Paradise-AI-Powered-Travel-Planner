import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
import os
import random
import requests

os.environ['GOOGLE_API_KEY'] = 'YOUR API KEY'  
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")
UNSPLASH_ACCESS_KEY = "YOUR API KEY"
YOUTUBE_API_KEY = "YOUR API KEY"

st.title('🌍 Journey to Paradise: Your AI Travel Buddy')


st.sidebar.title("✈️ Choose Your Adventure")
option = st.sidebar.radio("Select an option:", ["Plan My Own Trip", "Surprise Me!"])


def get_unsplash_image(destination):
    url = f"https://api.unsplash.com/photos/random?query={destination}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url).json()
    return response.get("urls", {}).get("regular", "")


def get_youtube_video(destination):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={destination}+travel+guide&type=video&key={YOUTUBE_API_KEY}&maxResults=1"
    response = requests.get(search_url).json()
    if "items" in response and len(response["items"]) > 0:
        video_id = response["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/embed/{video_id}"
    return ""


def estimate_travel_costs(distance):
    flight_cost = max(50, distance * 0.15 * 10)  
    train_cost = max(20, distance * 0.08 * 10)  
    bus_cost = max(10, distance * 0.05 * 10)   
    car_cost = max(15, distance * 0.12 * 10)    
    return flight_cost, train_cost, bus_cost, car_cost

if option == "Plan My Own Trip":
    st.subheader('🛫 Plan Your Own Trip')
    origin_country = st.text_input('🌎 Where would you like to start your journey?')
    destination_country = st.text_input('🗺️ Where would you like to go?')
    num_days = st.number_input('📅 How many days will you travel?', min_value=1, step=1)
    budget = st.slider('💰 Select Your Budget (₹)', min_value=1000, max_value=100000, step=1000, value=50000)
    
    travel_preferences = st.text_area('🎭 Describe your travel preferences (e.g., adventure, relaxation, culture, budget-friendly)')
    
    if st.button('✨ Plan My Trip'):
        if origin_country and destination_country and num_days:
            user_input = f"I am traveling from {origin_country} to {destination_country} for {num_days} days and a budget of {budget}. I prefer {travel_preferences}. Give me a detailed travel itinerary."
            messages = [
                SystemMessage(content="You are an expert travel planner AI. Provide detailed itineraries, including transportation, accommodations, and must-visit places."),
                HumanMessage(content=user_input)
            ]
            response = llm.invoke(messages)

            st.subheader('🗺️ Your AI-Generated Travel Plan:')
            st.write(response)
            
            distance = random.uniform(500, 8000)  
            flight, train, bus, car = estimate_travel_costs(distance)
            st.subheader('💰 Estimated Travel Costs:')
            st.write(f'✈️ Flight: ₹{flight:.2f}')
            st.write(f'🚆 Train:  ₹{train:.2f}')
            st.write(f'🚌 Bus:  ₹{bus:.2f}')
            st.write(f'🚗 Car:  ₹{car:.2f}')
            
            unsplash_image_url = get_unsplash_image(destination_country)
            if unsplash_image_url:
                st.image(unsplash_image_url, caption=f"{destination_country} Travel Image", use_column_width=True)
            
            youtube_video_url = get_youtube_video(destination_country)
            if youtube_video_url:
                st.video(youtube_video_url)
        else:
            st.warning('⚠️ Please enter all details (origin, destination, and days).')

elif option == "Surprise Me!":
    st.subheader('🎉 Get a Surprise Trip Recommendation!')
    origin_country = st.text_input('🌎 Where are you starting your journey from?')
    num_days = st.number_input('📅 How many days will you travel?', min_value=1, step=1)
    budget = st.slider('💰 Select Your Budget (₹)', min_value=1000, max_value=100000, step=1000, value=50000)
    
    if st.button('🎲 Surprise Me!'):
        if origin_country:
            user_input = f"I am starting from {origin_country}, have {num_days} days, and a budget of ₹{budget}. Suggest a travel destination within India that fits my budget and time, and provide a detailed itinerary."
            messages = [
                SystemMessage(content="You are an expert travel planner AI. Suggest a surprise travel destination within India based on the user's budget, time, and starting location. Provide a full itinerary."),
                HumanMessage(content=user_input)
            ]
            response = llm.invoke(messages)
            suggested_destination = response.split('\n')[0].replace('Surprise Destination:', '').strip()

            st.subheader(f'🌟 Surprise Destination: {suggested_destination}')
            st.write(response)
            
            unsplash_image_url = get_unsplash_image(suggested_destination)
            if unsplash_image_url:
                st.image(unsplash_image_url, caption=f"{suggested_destination} Travel Image", use_column_width=True)
            
            youtube_video_url = get_youtube_video(suggested_destination)
            if youtube_video_url:
                st.video(youtube_video_url)
        else:
            st.warning('⚠️ Please enter your starting location.')
