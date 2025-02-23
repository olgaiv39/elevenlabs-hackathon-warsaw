import os
import argparse
from dotenv import load_dotenv
import fal_client
import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob

nltk.download('punkt')

load_dotenv()

fal_key = os.getenv('FAL_API_KEY')
if not fal_key:
    raise EnvironmentError("FAL_API_KEY is not set. Please check your .env file and ensure it contains 'FAL_API_KEY=your_api_key_here'.")

def on_queue_update(update):
    # Print log messages as the fal_client job is in progress.
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

def find_attractive_moments(story, n=5):
    """
    Splits the story into sentences and scores each based on sentiment polarity.
    Returns up to n sentences with the highest absolute polarity (indicating dramatic moments).
    """
    sentences = sent_tokenize(story)
    scored_sentences = []
    for sentence in sentences:
        blob = TextBlob(sentence)
        # Use absolute polarity as a measure of emotional intensity
        score = abs(blob.sentiment.polarity)
        scored_sentences.append((sentence, score))
    
    # Sort sentences by score in descending order and select the top n
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    top_sentences = [s for s, score in scored_sentences[:n]]
    return top_sentences

def generate_illustration(prompt):
    """
    Calls the fal_client flux model with the provided prompt.
    """
    result = fal_client.subscribe(
        "fal-ai/flux/dev",
        arguments={
            "prompt": prompt
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Generate comic-style illustrations from attractive moments in a story."
    )
    parser.add_argument(
        "--story", type=str, default="",
        help="The story text to process. If not provided, the script will prompt for input."
    )
    parser.add_argument(
        "--story-file", type=str, default="",
        help="Path to a text file containing the story. If provided, this takes precedence over --story."
    )
    parser.add_argument(
        "--n", type=int, default=5,
        help="Number of attractive moments to select (default 5)."
    )
    args = parser.parse_args()

    if args.story_file:
        try:
            with open(args.story_file, 'r') as f:
                story = f.read()
        except Exception as e:
            print(f"Error reading story file: {e}")
            return
    elif args.story:
        story = args.story
    else:
        story = input("Enter the story text: ")

    # Evaluate and find the most attractive (emotionally charged) moments
    moments = find_attractive_moments(story, n=args.n)
    print("Attractive moments found:")
    for idx, moment in enumerate(moments, 1):
        print(f"{idx}. {moment}")
    
    # For each attractive moment, generate a comic-style illustration
    illustrations = {}
    for idx, moment in enumerate(moments, 1):
        prompt = f"Create a comic style illustration for the following scene: {moment}"
        print(f"\nGenerating illustration for moment {idx}:")
        print(f"Prompt: {prompt}")
        illustration_result = generate_illustration(prompt)
        illustrations[f"moment_{idx}"] = illustration_result
        print("Result:", illustration_result)
    
    print("\nAll illustration results:")
    print(illustrations)

if __name__ == "__main__":
    main()
