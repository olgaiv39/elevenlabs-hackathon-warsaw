import os
import re
import uuid
import nltk
import fal_client
from nltk.tokenize import sent_tokenize
from textblob import TextBlob

# Ensure required NLTK data is downloaded.
nltk.download('punkt')

class ImgGen:
    def __init__(self, fal_key: str):
        self.fal_key = fal_key

    def on_queue_update(self, update):
        """Print log messages while the fal_client job is in progress."""
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(log["message"])

    def evaluate_attractive_moments(self, story: str, images_per_chapter: int = 3) -> dict:
        """
        Splits the story based on chapter-end markers and selects up to 'images_per_chapter'
        of the most emotionally charged sentences per chapter.
        Chapter end markers include phrases such as:
          - "Chapter 1 ends"
          - "Chapter 2 has come to an end"
          - "Congratulations! You have finished Chapter 3!"
        If no markers are found, the entire story is treated as a single chapter.
        Returns a dictionary with keys as chapter labels and values as lists of selected sentences.
        """
        pattern = r'(Chapter \d+ (?:ends|has come to an end)|Congratulations! You have finished Chapter \d+!)'
        segments = re.split(pattern, story)
        chapters = []
        if len(segments) > 1:
            for i in range(1, len(segments), 2):
                chapter_text = segments[i - 1].strip()
                if chapter_text:
                    chapters.append(chapter_text)
        else:
            chapters.append(story)
        
        chapter_moments = {}
        for i, chapter in enumerate(chapters, 1):
            sentences = sent_tokenize(chapter)
            scored_sentences = []
            for sentence in sentences:
                blob = TextBlob(sentence)
                score = abs(blob.sentiment.polarity)
                scored_sentences.append((sentence, score))
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            top_sentences = [s for s, _ in scored_sentences[:images_per_chapter]]
            chapter_moments[f"chapter_{i}"] = top_sentences
        return chapter_moments

    def generate_illustration(self, prompt: str) -> str:
        """
        Calls the FAL flux model via fal_client.subscribe to generate a comic-style illustration.
        The generated image is saved to a temporary folder and its URL is returned.
        """
        result = fal_client.subscribe(
            "fal-ai/flux/dev",
            arguments={"prompt": prompt},
            with_logs=True,
            on_queue_update=self.on_queue_update,
        )
        # Create (if needed) a temporary directory to store generated images.
        temp_dir = os.path.join(os.getcwd(), "temp_images")
        os.makedirs(temp_dir, exist_ok=True)
        filename = f"{uuid.uuid4()}.png"
        file_path = os.path.join(temp_dir, filename)
        
        # Assume result contains binary image data. It might be a dict with 'image_bytes'.
        if isinstance(result, dict) and "image_bytes" in result:
            image_bytes = result["image_bytes"]
        else:
            image_bytes = result  # fallback if result is raw binary data
        
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        
        # Return the URL to access the image.
        # Ensure your Flask app serves the "temp_images" folder as static files.
        image_url = f"/temp_images/{filename}"
        return image_url

    def process_story(self, story: str, images_per_chapter: int = 3) -> dict:
        """
        Processes the story by:
          1. Splitting it into chapters and selecting attractive moments.
          2. Generating a comic-style illustration for each attractive moment.
        Returns a dictionary mapping each chapter to a list of image URLs.
        """
        chapter_moments = self.evaluate_attractive_moments(story, images_per_chapter)
        print("Attractive moments found per chapter:")
        for chapter, moments in chapter_moments.items():
            print(f"{chapter}:")
            for idx, moment in enumerate(moments, 1):
                print(f"  {idx}. {moment}")

        illustrations = {}
        for chapter, moments in chapter_moments.items():
            illustrations[chapter] = []
            for idx, moment in enumerate(moments, 1):
                prompt = f"Create a comic style illustration for the following scene: {moment}"
                print(f"\nGenerating illustration for {chapter} moment {idx}:")
                print(f"Prompt: {prompt}")
                image_url = self.generate_illustration(prompt)
                illustrations[chapter].append(image_url)
                print("Generated image URL:", image_url)
        return illustrations
