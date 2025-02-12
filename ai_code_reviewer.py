import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAXehSIPZDaWAbFE8xavz-rrEO-rPXPKAw")

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

# Streamlit UI
st.title("AI Code Reviewer")
st.write("Submit your Python code for review and receive suggestions for fixes.")

# Code input area
code_input = st.text_area("Enter your Python code here:", height=200)

if st.button("Review Code"):
    if code_input.strip():
        with st.spinner("Reviewing your code..."):
            try:
                review_feedback = get_code_review(code_input)
                st.subheader("Code Review Feedback")
                st.text_area("Feedback:", review_feedback, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some Python code before submitting.")
