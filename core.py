import os
import logging
from mistral import Mistral

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
NARRATOR_API_ID = os.environ["NARRATOR_API_ID"]

client = Mistral(api_key=MISTRAL_API_KEY)

def get_assistant_response(messages):
    """
    Given a list of messages representing the conversation history,
    including the latest user message, returns the assistant's response.

    Args:
        messages (list): List of dictionaries with 'role' (e.g., 'user', 'assistant') 
                         and 'content' (the message text).

    Returns:
        dict: Dictionary with 'role' set to 'assistant' and 'content' set to the 
              assistant's response text.

    Note:
        The frontend should handle the exit condition, e.g., by checking if the user
        input is "exit" and not calling this function if so.
    """
    logger.info("get_assistant_response called with %d messages", len(messages))
    # Call the Mistral API with the current conversation history
    chat_response = client.agents.complete(
        agent_id=NARRATOR_API_ID,
        messages=messages,
    )
    
    assistant_message = chat_response.choices[0].message
    logger.info("Received response from API: %s", assistant_message.content)
    
    return {"role": "assistant", "content": assistant_message.content}