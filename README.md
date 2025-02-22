# elevenlabs-hackathon-warsaw

The main goal of this project to extend boundaries of the story and provide user with unique experience. Meet firs narration extended story telling game.

# Objective

Using LLM agents and Elevenlabs product is being developed. The product provides opportunity for the player to get into the story and alter that in any way possible without being attached to certain scripts. Game is guided by voice, interacts witht the user and asks which actions user want to perform. Based on actions taken the further plot gets adjusted.

# Data

Currently the solution uses whatever Mistral was trained with. No additional fine tuning is made. 

# Architecture

The project is a conversation with and agent which is set to create creative stories according to the script.
1. Conversation happens via the chat written with Flask.
2. Agent responses according to the scrip. Proposing the user to make a descision.

# Summary