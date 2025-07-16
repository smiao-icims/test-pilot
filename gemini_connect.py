

import os
import google.generativeai as genai

# The script will automatically look for the GOOGLE_API_KEY environment variable.
# If you don't set the environment variable, you can configure the key directly like this:
# genai.configure(api_key="YOUR_API_KEY")

try:
    # Set up the model
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }

    model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                                  generation_config=generation_config)

    # Start a conversation
    convo = model.start_chat(history=[])

    # Send a message
    prompt = "Hello! Write a short, 1-paragraph poem about coding."
    print(f"User: {prompt}\n")
    convo.send_message(prompt)

    # Print the response
    print(f"Gemini: {convo.last.text}")

except Exception as e:
    print(f"An error occurred: {e}")
    print("\nPlease make sure you have set your GOOGLE_API_KEY environment variable correctly.")
    print("You can get a key from Google AI Studio.")


