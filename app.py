import streamlit as st
import google.generativeai as genai
import os
import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play

# Set up Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAX0RTZJ9eh3CV6seGCoidVc9pEL8JTySg"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize the generative model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Global variable to store conversation history
conversation_history = []

# Function for voice recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the speech."
    except sr.RequestError:
        return "Error with the speech recognition service."

# Voice assistance function
def voice_assistance(user_input):
    global conversation_history

    # Improved prompt for concise answers
    prompt = f"""
    You are an AI assistant in a conversation. The user asked:
    '{user_input}'
    Provide a clear and concise response without unnecessary elaboration.
    """

    response = model.generate_content(prompt).text

    # Store conversation history
    conversation_history.append({'user': user_input, 'ai': response})

    return response

# Streamlit UI
st.title("🎙️ AI Voice Assistant Chatbot")

# Button for voice input
if st.button("🎤 Speak Now"):
    user_input = recognize_speech()
    if user_input:
        st.write(f"**You:** {user_input}")
        response = voice_assistance(user_input)
        st.write(f"**AI:** {response}")

# Conversation history display
if conversation_history:
    st.subheader("📝 Conversation History")
    for chat in conversation_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**AI:** {chat['ai']}")