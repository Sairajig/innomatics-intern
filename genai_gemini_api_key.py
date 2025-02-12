import google.generativeai as genai
from IPython.display import Markdown, display

# Configure Gemini API
genai.configure(api_key="AIzaSyAXehSIPZDaWAbFE8xavz-rrEO-rPXPKAw")  # Replace with your actual key

# System prompt
sys_prompt = """You are a helpful data science tutor. You can only resolve data science related queries.
In case if someone has queries which are not relevant to data science, politely tell them to ask relevant queries only.
"""

# Initialize the model
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-exp", 
                              system_instruction=sys_prompt)

# Get user input
user_prompt = input("Enter your query: ")

# Generate response
response = model.generate_content(user_prompt)

# Display response (Markdown is optional for VS Code)
print("\nAI Response:\n")
print(response.text)
