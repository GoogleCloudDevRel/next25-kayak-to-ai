import time
import logging
import json
import sys
import os
from dotenv import load_dotenv

from google.cloud import pubsub_v1
from motor import move_motor
from phidgets import control_light

load_dotenv()  # Load environment variables from .env

# Configure logging to only use stdout/stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  # Log to console (stdout)
)

# Environment variables for Pub/Sub
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID")
COMPLETION_TOPIC_ID = os.environ.get("PUBSUB_COMPLETION_TOPIC_ID")

# Initialize Pub/Sub clients
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

# Construct subscription and topic paths
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
completion_topic_path = publisher.topic_path(PROJECT_ID, COMPLETION_TOPIC_ID)


def process_message(message):
    """
    Placeholder for actions to be performed based on the message content.
    """
    logging.info(f"Processing message: {message.data.decode('utf-8')}")

    data = json.loads(message.data.decode("utf-8"))
    if data["location"]:
        print(f" Received location: {data['location']}, location_id: {data['location_id']}")
        move_motor(data["location"]["location_id"])
        control_light(data["location"]["location_id"])
    else:
        raise ValueError('no location data was sent')

    logging.info(f"Finished processing message: {message.data.decode('utf-8')}")


def send_completion_message(message_id):
    """
    Sends a message to the completion topic indicating that the operation is complete.
    """
    message_data = f"Operation for message {message_id} completed."
    future = publisher.publish(completion_topic_path, message_data.encode("utf-8"))
    logging.info(
        f"Sent completion message for {message_id} with message_id: {future.result()}"
    )


def callback(message):
    """
    Callback function to handle received messages.
    """
    logging.info(f"Received message: {message.data.decode('utf-8')}")
    try:
        process_message(message)  # Call the imported function
        send_completion_message(message.message_id)
        message.ack()
        logging.info(f"Message {message.message_id} acknowledged.")
    except Exception as e:
        logging.error(f"Error processing message {message.message_id}: {e}")
        # Consider nacking the message here if you want it to be redelivered
        # message.nack()


def main():
    logging.info("Starting my_app service...")
    try:
        # Start the subscriber
        streaming_pull_future = subscriber.subscribe(
            subscription_path, callback=callback
        )
        logging.info(f"Listening for messages on {subscription_path}...")

        # Keep the main thread alive to continue receiving messages
        while True:
            time.sleep(60)  # Check every 60 seconds for any issues
    except KeyboardInterrupt:
        logging.info("Stopping my_app service...")
        streaming_pull_future.cancel()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        streaming_pull_future.cancel()
    finally:
        logging.info("my_app service stopped.")


if __name__ == "__main__":
    main()
