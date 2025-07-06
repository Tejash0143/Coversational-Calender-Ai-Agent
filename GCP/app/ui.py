import streamlit as st
from app.chat import get_response

def render_chat_ui():
    st.title("TailorTalk - Appointment Booking Assistant")
    st.subheader("Book your appointment via chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Type your message..."):
        # 1️⃣ Add the user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2️⃣ Call get_response with entire history
        assistant_reply = get_response(st.session_state.messages)

        # 3️⃣ Add assistant reply to history
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        # 4️⃣ Display assistant reply
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
