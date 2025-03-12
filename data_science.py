import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

API_KEY = "YOUR_GOOGLE_API_KEY"  
if not API_KEY:
    st.error("⚠️ GOOGLE_API_KEY is missing! Please set it in the script.")
else:
    os.environ["GOOGLE_API_KEY"] = API_KEY
st.set_page_config(page_title="Conversational AI Data Science Tutor", layout="wide")
col1, col2 = st.columns([4,1])
with col1:
    st.title("🧠 Conversational AI Data Science Tutor")
with col2:
    col2_left, col2_right = st.columns(2)
    with col2_left:
        show_history = st.button("📜 History")
    with col2_right:
        if st.button("🗑️ Clear"):
            st.session_state['chat_history'] = []
            st.session_state.memory.clear()
            st.rerun()

st.write("This AI tutor is designed to resolve your data science doubts using Gemini 1.5 Pro and memory capabilities.")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'show_history_state' not in st.session_state:
    st.session_state['show_history_state'] = False
if show_history:
    st.session_state['show_history_state'] = not st.session_state['show_history_state']
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        max_output_tokens=2048,
    )
    conversation = ConversationChain(
        llm=llm, 
        memory=st.session_state.memory,
        verbose=True
    )
except Exception as e:
    st.error(f"🚨 Error initializing AI model: {e}")
    conversation = None
user_input = st.text_input("Ask a Data Science Question:", key="input")
submit = st.button("Ask the Question")
if submit and user_input and conversation:
    with st.spinner('Thinking... 🤔'):
        try:
            response = conversation.predict(input=user_input)
            st.session_state.memory.save_context({'input': user_input}, {'output': response})
            st.session_state['chat_history'].append(("You", user_input))
            st.session_state['chat_history'].append(("Bot", response))
            st.subheader("🤖 AI Response:")
            st.write(response)
            if "```python" in response:
                st.subheader("🚀 Execute Code")
                code = response.split("```python")[1].split("```")[0]
                if st.button("Run Code"):
                    try:
                        with st.spinner('Executing code...'):
                            # Create a new code block with the executed results
                            exec_locals = {}
                            exec(code, globals(), exec_locals)
                            st.code(code, language='python')
                            if 'plt' in exec_locals:
                                st.pyplot(exec_locals['plt'])
                    except Exception as e:
                        st.error(f"Error executing code: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
if st.session_state['show_history_state'] and st.session_state['chat_history']:
    st.sidebar.subheader("📜 Chat History:")
    for role, text in st.session_state['chat_history']:
        if role == "You":
            st.sidebar.markdown(f"""
            <div style='background-color: #1a1a1a; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #333'>
                <b>{role}:</b> {text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"""
            <div style='background-color: #2b2b2b; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #333'>
                <b>{role}:</b> {text}
            </div>
            """, unsafe_allow_html=True)
if st.session_state['show_history_state']:
    st.sidebar.subheader("📜 Chat History:")
    if st.sidebar.button("💾 Export Chat"):
        chat_export = "\n\n".join([f"{role}: {text}" for role, text in st.session_state['chat_history']])
        st.sidebar.download_button(
            label="Download Chat",
            data=chat_export,
            file_name="chat_history.txt",
            mime="text/plain"
        )
