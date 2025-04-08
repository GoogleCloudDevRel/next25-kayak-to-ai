from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai.types import HttpOptions, Part
from dotenv import load_dotenv
import os
from google.cloud import pubsub_v1
from uuid import uuid4
import logging
import sys
import json


# Load environment variables from .env
load_dotenv()

# Configure logging to only use stdout/stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  # Log to console (stdout)
)

# Initialize Gemini client
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(http_options=HttpOptions(api_version="v1"))
GEMINI_MODEL = "gemini-2.0-flash"

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PUBSUB_TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID")
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

# initialize sub client
subscriber = pubsub_v1.SubscriberClient()
SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID")
subscription_path = subscriber.subscription_path(GOOGLE_CLOUD_PROJECT, SUBSCRIPTION_ID)


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://kayak-frontend-78192108242.us-central1.run.app"]}})


def publish_message(topic_path, message):
    """Publishes a message to a Pub/Sub topic."""
    future = publisher.publish(topic_path, message.encode("utf-8"))
    print(f"Published message id {future.result()}")

    return future.result()

@app.route("/")
def index():
    return jsonify({"message": "Root endpoint"})


prompt_template = """
    You are an expert kayak guide around Lake Washington in Seattle, WA.
    A user has requested the following: {prompt}. 
    Using your best knowledge about the 9 locations that you can kayak to below,
    return the single best location from the list, name only. The available list
    of locations is:
    - Virginia Mason Athletic Center,
    - Seward Park,
    - Magnuson Cafe and Brewery,
    - Luther Burbank Park,
    - Kirkland Urban,
    - Woodmark Hotel and Spa,
    - Daniel's Broiler,
    - University of Washington Husky Stadium,
    - Fremont Troll
    """

@app.route("/api/process-prompt", methods=["POST"])
def process_prompt():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        print(f"prompt: {prompt}")

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        formatted_template = prompt_template.format(prompt=prompt)
        

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=formatted_template,
        )

        # Extract the text content from the response
        text_response = response.text

        print(text_response)

        with open('locations.json','r') as file:
            locations = json.load(file)
        
        counter = 0
        while True:
            for l in locations:
                print(l)
                if text_response.rstrip().lstrip() == l['name']:
                    print(f"found {text_response}")
                    location_requested = l['name']
                    break
            response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=f"{formatted_template}. The value {text_response} was not in the list, try again.",
            )
            text_response = response.text
            counter += 1
            if counter >= 5:
                break

        return jsonify({"location": location_requested})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/get-code", methods=["POST"])
def get_code():
    data = request.get_json()
    location = data.get("location")
    prompt = data.get("prompt")

    return jsonify({"message": "Sample Code"})


@app.route("/api/move-kayak", methods=["POST"])
def move_kayak():
    data = request.get_json()
    destination = data.get("destination")

    if not destination:
        return jsonify({"error": "Destination is required"}), 400
    
    submit_data = {
        "location": data.get("destination"),
        "uuid": uuid4().hex
    }

    topic_path = publisher.topic_path(GOOGLE_CLOUD_PROJECT, PUBSUB_TOPIC_ID)
    message_id = publish_message(topic_path, submit_data)

    # listen for the message back
    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback(message_id)
    )
    logging.info(f"Listening for messages on {subscription_path}...")

    return jsonify({"message": "Moved kayak to " + destination})

def callback(message, message_id):
    """
    Callback function to handle received messages.
    """
    logging.info(f"Received message: {message.data.decode('utf-8')}")
    try:
        if message.message_id == message_id:
            message.ack()
        else: 
            message.nack()
        logging.info(f"Message {message.message_id} acknowledged.")
    except Exception as e:
        logging.error(f"Error processing message {message.message_id}: {e}")
        message.nack()

if __name__ == "__main__":
    # You can specify host='0.0.0.0' if you want it accessible externally
    app.run(debug=True, port=5000)


# 4. based on the location information, run the kayak
# 5. return complete when complete