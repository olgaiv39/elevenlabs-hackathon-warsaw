# elevenlabs-hackathon-warsaw

The primary goal of this project is to push the boundaries of interactive storytelling and offer users a truly unique experience. Introducing our first narration-extended storytelling game.

# Objective

Using Large Language Model (LLM) agents in conjunction with the ElevenLabs platform, we are developing a dynamic, voice-guided storytelling experience. This approach enables players to immerse themselves in the narrative, make impactful decisions, and shape the story—free from rigid, predetermined scripts. Additionally, the application monitors inference speed, providing valuable data for model benchmarking.

# Architecture

This project revolves around a conversational agent programmed to generate creative narratives based on a guiding script:

1. Chat Interface: All interactions take place through a Flask-based chat interface.
2. Decision-Making: The agent follows a core script but prompts the user to make decisions at critical points, thereby influencing the direction of the story.

To create this project we were using:
- Lovable for the front-end
- Mistral as main narration agent
- Elevenlabs for voice acting
- Fal.ai (Flux model) for image generation

# Summary

Designed to run locally by default, this application can also be easily deployed to the cloud. By combining two generative models, it delivers a one-of-a-kind user experience while simultaneously allowing performance benchmarking of these models.