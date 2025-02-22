import os
import json
import logging
import re
from bs4 import BeautifulSoup


def main():
    logging.basicConfig(
        filename="script.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logging.info("Starting the HTML parsing script.")

    try:
        with open("config.json", "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            logging.info("Successfully loaded config.json")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading config.json: {e}")
        raise

    raw_path = config.get("data_raw")
    clean_path = config.get("data_clean")

    if not raw_path or not clean_path:
        logging.error("Missing 'data_raw' or 'data_clean' in config.json")
        raise ValueError("Config file must contain 'data_raw' and 'data_clean' paths.")

    os.makedirs(clean_path, exist_ok=True)

    if os.path.isdir(raw_path):
        html_files = [f for f in os.listdir(raw_path) if f.endswith(".html")]

        if not html_files:
            logging.error(f"No HTML files found in directory: {raw_path}")
            raise FileNotFoundError(f"No HTML files found in {raw_path}")

        logging.info(f"Found {len(html_files)} HTML files in {raw_path}. Processing...")

        for html_file in html_files:
            html_file_path = os.path.join(raw_path, html_file)
            text_file_name = os.path.splitext(html_file)[0] + ".txt"
            text_file_path = os.path.join(clean_path, text_file_name)

            if os.path.exists(text_file_path):
                logging.info(f"Skipping {html_file} as {text_file_name} already exists.")
                continue

            try:
                with open(html_file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
                    logging.info(f"Successfully read HTML file: {html_file_path}")

                soup = BeautifulSoup(html_content, "html.parser")
                plain_text = soup.get_text(separator="\n", strip=True)

                cleaned_text = re.sub(r"\[\d+\]", "", plain_text)

                with open(text_file_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(cleaned_text)
                    logging.info(f"Extracted text saved to {text_file_path}")

            except Exception as e:
                logging.error(f"Error processing {html_file_path}: {e}")
                continue

    else:
        logging.error(f"Invalid data_raw path: {raw_path} is not a directory.")
        raise NotADirectoryError(f"'{raw_path}' is not a directory.")

    logging.info("Script execution completed successfully.")
    print(f"Processed {len(html_files)} HTML files. Extracted text saved in {clean_path}.")


if __name__ == "__main__":
    main()