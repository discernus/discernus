#!/usr/bin/env python3
"""
PDF to Text Extractor
Extracts text content from PDF files and saves as plain text.
"""

import pdfplumber
import sys
import os

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Extracted text content
    """
    text_content = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Processing PDF with {len(pdf.pages)} pages...")

            for i, page in enumerate(pdf.pages):
                print(f"Extracting text from page {i + 1}/{len(pdf.pages)}...")
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)

        return "\n\n".join(text_content)

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def main():
    # Path to the PDF file
    pdf_path = "/Volumes/code/discernus/pm/populism/databases/brazil_2018/populism-in-brazils-2018-general-elections.pdf"

    # Generate output text file path
    output_path = pdf_path.replace('.pdf', '.txt')

    print(f"Extracting text from: {pdf_path}")
    print(f"Output will be saved to: {output_path}")

    # Extract text
    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text:
        # Save to text file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)

        print(f"✓ Successfully extracted {len(extracted_text)} characters")
        print(f"✓ Text saved to: {output_path}")
    else:
        print("✗ Failed to extract text from PDF")
        sys.exit(1)

if __name__ == "__main__":
    main()

