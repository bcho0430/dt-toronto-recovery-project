import os
import requests
import pandas as pd
import fitz  # PyMuPDF
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the CSV file
df = pd.read_csv('london_aspx_links.csv', sep=',')

# Filter out NaN values in the Link column
df = df.dropna(subset=['Link'])

# Directory to save the downloaded PDF files
pdf_dir = 'aspx_files'

# Create directory if it doesn't exist
os.makedirs(pdf_dir, exist_ok=True)

def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            logging.warning(f"Failed to download {url} with status code {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Exception occurred while downloading {url}: {e}")
        return False

def pdf_to_text(pdf_path):
    text = ""
    try:
        document = fitz.open(pdf_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
    except Exception as e:
        logging.error(f"Failed to extract text from {pdf_path}: {e}")
    return text

# Name of the combined text file
combined_file_path = 'combined_aspx.txt'

# Set to keep track of unique text blocks
unique_text_blocks = set()

# Open the combined text file in write mode
with open(combined_file_path, 'w', encoding='utf-8') as combined_file:
    for index, row in df.iterrows():
        url = row['Link']
        logging.info(f"Processing URL: {url}")
        
        # Ensure the URL is a string
        if not isinstance(url, str):
            logging.warning(f"Invalid URL at index {index}: {url}")
            continue
        
        # Extract the PDF file name from the URL
        pdf_file_name = url.split('/')[-1]
        pdf_file_path = os.path.join(pdf_dir, pdf_file_name)
        
        # Download the PDF file
        if download_pdf(url, pdf_file_path):
            # Convert the PDF to text
            text_content = pdf_to_text(pdf_file_path)
            
            # Split text content into blocks (e.g., paragraphs or lines)
            text_blocks = text_content.split("\n")
            
            for block in text_blocks:
                # Strip whitespace and ignore empty blocks
                block = block.strip()
                if block and block not in unique_text_blocks:
                    unique_text_blocks.add(block)
                    combined_file.write(block + "\n")

logging.info(f"All unique text has been combined into {combined_file_path}")