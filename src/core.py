import os
import logging
from dotenv import load_dotenv
from mistralai import Mistral


class Core:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        load_dotenv()
        self.mistral_api_key = os.environ["MISTRAL_API_KEY"]
        self.narrator_api_id = os.environ["NARRATOR_API_ID"]
        
        self.client = Mistral(api_key=self.mistral_api_key)
        self.initial_message = {"role": "user", "content": "Start a new story."}
        
    def start_conversation(self) -> list:
        """
        Starts a new conversation by sending an initial user message and returning the initial conversation history,
        including the initial user message and the assistant's response.

        Returns:
            list: List containing the initial user message and the assistant's response.
        """
        self.logger.info("Starting new conversation")
        initial_user_message = self.initial_message
        assistant_response = self.get_assistant_response([initial_user_message])
        return [initial_user_message, assistant_response]

    def get_assistant_response(self, messages: list) -> dict:
        """
        Given a list of messages representing the conversation history (including the latest user message),
        returns the assistant's response by calling the Mistral API.

        Args:
            messages (list): List of dictionaries with 'role' (e.g., 'user', 'assistant') 
                             and 'content' (the message text).

        Returns:
            dict: Dictionary with 'role' set to 'assistant' and 'content' set to the assistant's response text.
        """
        self.logger.info("get_assistant_response called with %d messages", len(messages))
        # Call the Mistral API with the conversation history
        chat_response = self.client.agents.complete(
            agent_id=self.narrator_api_id,
            messages=messages,
        )
        
        assistant_message = chat_response.choices[0].message
        self.logger.info("Received response from API: %s", assistant_message.content)
        
        return {"role": "assistant", "content": assistant_message.content}
