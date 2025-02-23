import os
import re
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
        # Regular expression to match chapter-end phrases.
        pattern = r'(Chapter \d+ (?:ends|has come to an end)|Congratulations! You have finished Chapter \d+!)'
        segments = re.split(pattern, story)
        chapters = []
        if len(segments) > 1:
            # There are chapter markers: each chapter is the text immediately before a marker.
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
                # Use the absolute sentiment polarity as a proxy for emotional intensity.
                score = abs(blob.sentiment.polarity)
                scored_sentences.append((sentence, score))
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            # Select up to 'images_per_chapter' sentences for each chapter.
            top_sentences = [s for s, _ in scored_sentences[:images_per_chapter]]
            chapter_moments[f"chapter_{i}"] = top_sentences
        return chapter_moments

    def generate_illustration(self, prompt: str):
        """
        Calls the fal.ai flux model via fal_client.subscribe to generate a comic-style illustration.
        """
        result = fal_client.subscribe(
            "fal-ai/flux/dev",
            arguments={"prompt": prompt},
            with_logs=True,
            on_queue_update=self.on_queue_update,
        )
        return result

    def process_story(self, story: str, images_per_chapter: int = 3) -> dict:
        """
        Combines the evaluation and illustration steps:
          1. Splits the story into chapters and evaluates each to find attractive moments.
          2. Generates comic-style illustrations for each attractive moment.
        Returns a dictionary mapping each chapter to a list of illustration results.
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
                result = self.generate_illustration(prompt)
                illustrations[chapter].append(result)
                print("Result:", result)
        return illustrations
