from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables (API key)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the chat model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# Create a message
message = HumanMessage(
    content="Translate the following English text to French: 'Hello, how are you?'"
)

# Invoke the model
result = llm.invoke([message])

# Print the response
print(result.content)
