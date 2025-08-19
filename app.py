import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Avatar paths
avatars = {
    "assistant": "images/user.png",  # Replace with your logo
    "user": "images/user2.png"       # Replace with user avatar
}

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello 👋 How may I assist you today?"}
    ]

# Function to generate AI response
def generateResponse(input_text):
    try:
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        if not GEMINI_API_KEY:
            return "❌ GEMINI_API_KEY not found in .env file"

        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)

        # Use text-only model
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(input_text)
        return response.text if hasattr(response, "text") else "⚠️ No response from model."

    except Exception as ex:
        return f"❌ Error: {ex}"


def main():
    st.set_page_config(page_title="AI Chatbot", initial_sidebar_state="auto")
    st.markdown("""
    <div style='text-align:center;'>
        <h1 style='color:#3184a0; margin-bottom:0;'>CHATBOT</h1>
        <h3 style='color:#0b2c6e; margin-top:2px;'>AI Chatbot</h3>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("images/user.png", use_container_width=True)
        st.button("🗑 Clear Chat History", on_click=clear_chat_history)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello 👋 How may I assist you today?"}
        ]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=avatars[message["role"]]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=avatars["user"]):
            st.write(prompt)

        # Assistant response
        with st.chat_message("assistant", avatar=avatars["assistant"]):
            with st.spinner("Thinking..."):
                response = generateResponse(prompt)
                st.write(response)

                # Save assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })


if __name__ == "__main__":
    main()
