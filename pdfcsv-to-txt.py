import os
import requests
import pandas as pd
import fitz  # PyMuPDF

# Load the CSV file
df = pd.read_csv('london_pdf_links.csv', sep=',')

# Filter out NaN values in the Link column
df = df.dropna(subset=['Link'])

# Directory to save the downloaded PDF files
pdf_dir = 'pdf_files'

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
            print(f"Failed to download {url}")
            return False
    except Exception as e:
        print(f"Exception occurred while downloading {url}: {e}")
        return False

def pdf_to_text(pdf_path):
    text = ""
    try:
        document = fitz.open(pdf_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
    except Exception as e:
        print(f"Failed to extract text from {pdf_path}: {e}")
    return text

# Name of the combined text file
combined_file_path = 'combined_pdf.txt'

# Open the combined text file in write mode
with open(combined_file_path, 'w', encoding='utf-8') as combined_file:
    for index, row in df.iterrows():
        url = row['Link']
        print(f"Processing URL: {url}")
        
        # Ensure the URL is a string
        if not isinstance(url, str):
            print(f"Invalid URL at index {index}: {url}")
            continue
        
        # Extract the PDF file name from the URL
        pdf_file_name = url.split('/')[-1]
        pdf_file_path = os.path.join(pdf_dir, pdf_file_name)
        
        # Download the PDF file
        if download_pdf(url, pdf_file_path):
            # Convert the PDF to text
            text_content = pdf_to_text(pdf_file_path)
            
            # Write the text content to the combined file
            combined_file.write(text_content)
            combined_file.write("\n")  # Optional: Add a newline between files

print(f"All text has been combined into {combined_file_path}")
