import os
from dotenv import load_dotenv
from llama_cloud import LlamaCloud

# Load the API key from your hidden .env file
load_dotenv()

# Initialize the client
client = LlamaCloud()

# Target your local PDF file
pdf_path = "./einleitung.pdf"

print("Uploading file to LlamaCloud...")
file = client.files.create(file=pdf_path, purpose="parse")

print("Processing file using Agentic AI Vision (this may take a minute)...")
result = client.parsing.parse(
    file_id=file.id,
    version="latest",
    expand=["markdown"],
    tier="agentic", 
    processing_options={
        "ocr_parameters": {
            "languages": ["de","la"]
        }
    },
    # FIXED: Changed key name from 'prompt' to 'custom_prompt'
    agentic_options={
        "custom_prompt": (
            "This document is an old German text written in Fraktur (blackletter) script. "
            "Carefully transcribe the historical typography into clean, modern German markdown text. "
            "Pay special attention to distinguishing the historical long 's' (ſ) from the letter 'f'. "
            "CRITICAL FORMATTING INSTRUCTIONS:\n"
            "1. REJOIN HYPHENATED WORDS: If a German word is broken across two lines with a hyphen (e.g., 'Ver-\nbindung'), "
            "rejoin it seamlessly into a single word ('Verbindung') on the same line to fix the paragraph flow.\n"
            "2. HANDLE SPERRDRUCK (LETTER-SPACED EMPHASIS): "
            "Identify words emphasized by letter-spacing, close the gaps, "
            "and mark emphasis using Markdown UNDERSCORES exclusively "
            "(e.g., _Gewinn_, _Geist_). "
            "Never use asterisks for emphasis. "
            "Reserve literal asterisks exclusively for historical footnote "
            "references and note labels, such as *), **), and ***). "
            "Preserve the exact number of asterisks in each footnote marker. "
            "Do not escape, superscript, italicize, or otherwise format "
            "footnote markers.\n"
            "4. PRESERVE NOTE BREAK: Many pages have a divider beginning at left margin separating main body from "
            "footnotes, preserve this with underscores ____. meanwhile there are a few linebreak markers"
            "centered, which should be replaced with the markdown ---- linebreak.\n"
            "5. PAGE NUMBERS: The top of a page has both page number and one or two numbers. "
            "The extra numbers are for the sections and should be omitted. "
            "The page numbers should be preserved as html comments. \n"
            "6. LANGUAGES: Greek can be left as it is in utf-8 but Latin i.e. roman letter sequences "
            "should be wrapped as html <span lang=\"la\"> and italics additionally in <i>"
        )
    }
)

# Extract and save the result
parsed_text = result.markdown.pages[0].markdown

# 1. Loop through all pages and stitch them together
full_document_text = ""

for pdf_page, page in enumerate(result.markdown.pages, start=1):
    if page.success:
        full_document_text += f"\n\n<!-- PDF_PAGE: {pdf_page} -->\n\n"
        full_document_text += page.markdown
        full_document_text += "\n\n"
        
# 2. Save the complete text to your markdown file
output_path = "./parsed_output.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_document_text)

print(f"Success! All {len(result.markdown.pages)} pages have been saved to: {output_path}")

