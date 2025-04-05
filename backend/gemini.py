import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model_name = "gemini-2.0-flash"

def get_location_details():
    """Get some details about a location."""
    print("LIGHTBOT: Lights enabled.")


def get_available_locatins():
    """Get a list of available locations."""
    print(f"LIGHTBOT: Lights set to.")


def set_destination():
    """Stop flashing lights."""
    print("LIGHTBOT: Lights turned off.")


kayak_controls = [get_location_details, get_available_locatins, set_destination]

# replace this prompt
instruction = "You are a helpful lighting system bot. You can turn lights on and off, and you can set the color. Do not perform any other tasks."

model = genai.GenerativeModel(
    model_name, tools=kayak_controls, system_instruction=instruction
)

chat = model.start_chat()