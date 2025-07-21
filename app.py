import streamlit as st
import google.generativeai as genai
import json
import os

# API Key (No security added as per request)
API_KEY = "your_api_key"
genai.configure(api_key=API_KEY)

# Set Page Config
st.set_page_config(page_title="ChatBot", page_icon="🤖", layout="wide")

# Title
st.title("🤖 AI ChatBot")
st.write("Chat with your AI Assistant!")

# Chat History File
CHAT_HISTORY_FILE = "chat_history.json"

# Load chat history from file (or create a new one)
if "chat_history" not in st.session_state:
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            st.session_state.chat_history = json.load(f)
    else:
        st.session_state.chat_history = {}

# Get chat IDs
chat_ids = list(st.session_state.chat_history.keys())

# Sidebar - Chat Management
with st.sidebar:
    st.subheader("Chat History")

    # Model Selection
    model_options = ["gemini-1.5-pro", "gemini-1.5-flash"]
    selected_model = st.selectbox("Select AI Model", model_options)

    # New Chat Button
    if st.button("+ New Chat", use_container_width=True):
        new_chat_id = str(len(chat_ids) + 1)
        st.session_state.chat_history[new_chat_id] = {
            "name": "New Chat",
            "messages": [],
            "model": selected_model  # Store selected model for this chat
        }
        st.session_state["current_chat"] = new_chat_id

        # Save to file
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump(st.session_state.chat_history, f)

        st.rerun()

    # Display previous chats
    for chat_id in chat_ids:
        chat_data = st.session_state.chat_history[chat_id]
        chat_name = chat_data["name"]

        col1, col2 = st.columns([4, 1])

        if col1.button(chat_name, key=f"chat_{chat_id}"):
            st.session_state["current_chat"] = chat_id
            st.rerun()

        with col2:
            if st.button("⋮", key=f"menu_{chat_id}"):
                st.session_state["show_menu"] = chat_id

        if "show_menu" in st.session_state and st.session_state["show_menu"] == chat_id:
            new_name = st.text_input(f"Rename {chat_name}:", value=chat_name, key=f"rename_{chat_id}")
            if st.button("Save", key=f"save_{chat_id}"):
                st.session_state.chat_history[chat_id]["name"] = new_name
                del st.session_state["show_menu"]

                with open(CHAT_HISTORY_FILE, "w") as f:
                    json.dump(st.session_state.chat_history, f)
                st.rerun()

            if st.button("🗑️ Delete", key=f"delete_{chat_id}"):
                del st.session_state.chat_history[chat_id]

                with open(CHAT_HISTORY_FILE, "w") as f:
                    json.dump(st.session_state.chat_history, f)

                if "current_chat" in st.session_state and st.session_state["current_chat"] == chat_id:
                    del st.session_state["current_chat"]

                st.rerun()

# Chat Window
if "current_chat" in st.session_state and st.session_state["current_chat"] in st.session_state.chat_history:
    chat_id = st.session_state["current_chat"]
    chat_data = st.session_state.chat_history[chat_id]

    # Display Chat Messages
    for msg in chat_data["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input Box
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Auto-generate chat name based on first message
        if chat_data["name"] == "New Chat" and len(chat_data["messages"]) == 0:
            chat_data["name"] = user_input[:30]  # First 30 characters as chat name

        # Store user message
        chat_data["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Select Model
        model_name = chat_data.get("model", "gemini-1.5-pro")

        # Generate AI Response
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(user_input)
            ai_response = response.text.strip() if response.text else "Sorry, I couldn't generate a response."
        except Exception as e:
            ai_response = f"Error: {str(e)}"

        # Store AI response
        chat_data["messages"].append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.write(ai_response)

        # Save updated chat history
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump(st.session_state.chat_history, f)
