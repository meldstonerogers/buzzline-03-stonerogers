"""
json_consumer_stonerogers.py

Consume json messages from a Kafka topic and process using Polars.

JSON is a set of key:value pairs. 

Example serialized Kafka message
"{\"message\": \"I love Python!\", \"author\": \"Eve\"}"

Example JSON message (after deserialization) to be analyzed
{"message": "I love Python!", "author": "Eve"}

"""

#####################################
# Import Modules
#####################################

# Import packages from Python Standard Library
import os
import json  # handle JSON parsing
# from collections import defaultdict  # data structure for counting author occurrences
import datetime

# Import external packages
import polars as pl 
from dotenv import load_dotenv

# Import functions from local modules
from utils.utils_consumer import create_kafka_consumer
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################


def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("BUZZ_TOPIC", "unknown_topic")
    logger.info(f"Kafka topic: {topic}")
    return topic


def get_kafka_consumer_group_id() -> int:
    """Fetch Kafka consumer group id from environment or use default."""
    group_id: str = os.getenv("BUZZ_CONSUMER_GROUP_ID", "default_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id


#####################################
# Set up Polars DataFrame to hold author counts
#####################################

# Aggregation using the groupby method

author_df = pl.DataFrame({
    "author": pl.Series(name="author", dtype=pl.Utf8),
    "count": pl.Series(name="count", dtype=pl.Int64),
    "timestamp": pl.Series(name="timestamp", dtype=pl.Datetime)  # Assuming timestamp is DateTime type
})

#####################################
# Function to process a single message
# #####################################


def process_message(message: str) -> None:
    """
    Process a single JSON message from Kafka and update Polars DataFrame with timestamps.

    Args:
        message (str): The JSON message as a string.
    """
    global author_df

    try:
        # Log the raw message for debugging
        logger.debug(f"Raw message: {message}")

        # Parse the JSON string into a Python dictionary
        message_dict: dict = json.loads(message)

        # Ensure the processed JSON is logged for debugging
        logger.info(f"Processed JSON message: {message_dict}")

        if isinstance(message_dict, dict):
            # Extract the 'author' field from the JSON message
            author = message_dict.get("author", "unknown")

            # Log received author
            logger.info(f"Message received from author: {author}")

            # Extract the 'timestamp' field, default to None if missing
            timestamp = message_dict.get("timestamp", None)  # This should be None if missing

            # Log received timestamp (if any)
            logger.info(f"Message received at timestamp: {timestamp}")

            # Create a new Polars DataFrame entry for this message
            new_entry = pl.DataFrame({
                "author": [author], 
                "count": [1], 
                "timestamp": [timestamp]  # Now using None for missing timestamp
            })

            # Append to the existing DataFrame
            author_df = pl.concat([author_df, new_entry])

            # Aggregate counts using Polars
            author_df = author_df.groupby("author").agg(pl.col("count").sum().alias("total_count"))

            # Log the updated counts
            logger.info(f"Updated author counts:\n{author_df}")
        else:
            logger.error(f"Expected a dictionary but got: {type(message_dict)}")

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON message: {message}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


#####################################
# Define main function for this module
#####################################


def main() -> None:
    """
    Main entry point for the consumer.

    - Reads the Kafka topic name and consumer group ID from environment variables.
    - Creates a Kafka consumer using the `create_kafka_consumer` utility.
    - Performs analytics on messages from the Kafka topic.
    """
    logger.info("START consumer.")

    # fetch .env content
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    logger.info(f"Consumer: Topic '{topic}' and group '{group_id}'...")

    # Create the Kafka consumer using the helpful utility function.
    consumer = create_kafka_consumer(topic, group_id)

    # Poll and process messages
    logger.info(f"Polling messages from topic '{topic}'...")
    try:
        for message in consumer:
            message_str = message.value
            logger.debug(f"Received message at offset {message.offset}: {message_str}")
            process_message(message_str)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info(f"Kafka consumer for topic '{topic}' closed.")

    logger.info(f"END consumer for topic '{topic}' and group '{group_id}'.")


#####################################
# Conditional Execution
#####################################

# Ensures this script runs only when executed directly (not when imported as a module).
if __name__ == "__main__":
    main()
