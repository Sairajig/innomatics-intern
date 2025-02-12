import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAXehSIPZDaWAbFE8xavz-rrEO-rPXPKAw")  # Replace with your actual API key

def get_code_review(code):
    """Send the code to Gemini API for review and get feedback."""
    prompt = f"""
    Review the following Python code and provide feedback on potential bugs, errors, and areas of improvement.
    Also, provide a corrected version of the code if necessary.
    
    Code:
    ```python
    {code}
    ```
    """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI with Centered Title
st.markdown(
    """
    <h1 style='text-align: center; color:rgb(1, 80, 252); font-size: 2.5em;'>🤖 AI Code Reviewer 📝</h1>
    <h3 style='text-align: center; color: #555;'>Analyze & Improve Your Python Code Instantly! 🚀</h3>
    <hr style="border: 1px solid #ddd;">
    """,
    unsafe_allow_html=True,
)

# Custom Styles
st.markdown(
    """
    <style>
        .stTextArea textarea {font-size: 1.2em; font-family: 'Courier New', monospace; }
        .stButton button { background-color:rgb(1, 80, 252); color: white; font-size: 1.2em; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.write("### 🔍 How It Works:")
st.markdown(
    """
    ✅ **Step 1:** Paste your Python code into the text box below. ⌨️  
    ✅ **Step 2:** Click the **Review Code** button. 🚀  
    ✅ **Step 3:** Get instant **bug fixes, improvements, and suggestions!** 🎯  
    """,
    unsafe_allow_html=True,
)

# Code input area
code_input = st.text_area("📌 Paste Your Python Code Here:", height=200, placeholder="Write or paste your Python code...")

if st.button("🚀 Review Code"):
    if code_input.strip():
        with st.spinner("🕵️‍♂️ Analyzing your code... Please wait!"):
            try:
                review_feedback = get_code_review(code_input)
                st.success("✅ Code review completed!")

                st.markdown("### 📢 **AI Code Review Feedback:**")
                st.text_area("📝 AI Suggestions:", review_feedback, height=300)
                
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter some Python code before submitting!")
