from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai.types import HttpOptions, Part
from dotenv import load_dotenv
import os
from google.cloud import pubsub_v1


# Load environment variables from .env
load_dotenv()

# Initialize Gemini client
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(http_options=HttpOptions(api_version="v1"))
GEMINI_MODEL = "gemini-2.0-flash"

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PUBSUB_TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID")
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://kayak-frontend-78192108242.us-central1.run.app"]}})


def publish_message(topic_path, message):
    """Publishes a message to a Pub/Sub topic."""
    future = publisher.publish(topic_path, message.encode("utf-8"))
    print(f"Published message id {future.result()}")


@app.route("/")
def index():
    return jsonify({"message": "Root endpoint"})


@app.route("/api/generate-location", methods=["POST"])
def test():
    return jsonify({"message": "Test endpoint"})


@app.route("/api/move-kayak", methods=["POST"])
def move_kayak():
    data = request.get_json()
    destination = data.get("destination")

    if not destination:
        return jsonify({"error": "Destination is required"}), 400

    topic_path = publisher.topic_path(GOOGLE_CLOUD_PROJECT, PUBSUB_TOPIC_ID)
    publish_message(topic_path, destination)

    # TODO: Implement logic to move the kayak
    return jsonify({"message": "Moving kayak to " + destination})


@app.route("/api/process-prompt", methods=["POST"])
def process_prompt():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        # Extract the text content from the response
        text_response = response.text

        return jsonify({"response": text_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def start_kayak():
    # TODO: Implement logic to start the kayak
    return jsonify({"message": "Kayak started"})


@app.route("/api/stop-kayak", methods=["POST"])
def stop_kayak():
    # TODO: Implement logic to stop the kayak
    return jsonify({"message": "Kayak stopped"})


@app.route("/api/get-status", methods=["GET"])
def get_status():
    # TODO: Implement logic to get the kayak status
    return jsonify({"status": "idle"})


@app.route("/api/get-location-details", methods=["POST"])
def get_location_details():
    data = request.get_json()
    location = data.get("location")
    if not location:
        return jsonify({"error": "Location is required"}), 400
    # TODO: Implement logic to get location details
    return jsonify({"location": location, "details": "Details for " + location})


if __name__ == "__main__":
    # You can specify host='0.0.0.0' if you want it accessible externally
    app.run(debug=True, port=5000)

# 1. user prompts to ask questions about where something is from
# 2. gemini returns responses
# 3. user picks location to go to
# 4. based on the location information, run the kayak
# 5. return complete when complete
# 6. display informaiton about the location@app.route('/api/start-kayak', methods=['POST'])