import cv2
import pytesseract
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

# Set Tesseract path manually
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load Excel file
file_path = r"D:\GameJam\Electrical_Symbol_Recognition\Files\436 Datalijst-kasten.xlsx"
xls = pd.ExcelFile(file_path)
lijst_df = xls.parse("Lijst")
kasten_df = xls.parse("Overzicht Kasten")
tabbladen_df = xls.parse("LS Tabbladen")

# OCR Processing Function
def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    text = pytesseract.image_to_string(gray, config='--psm 6')
    return text.strip()

# Function to find best match in Excel
def find_best_match(extracted_text, df, column_name):
    """Find the best matching entry from the given DataFrame column."""
    best_match, score = process.extractOne(extracted_text, df[column_name].dropna().astype(str))
    return best_match, score

# Comparison Function
def compare_with_excel(extracted_text):
    """Compare extracted text with Excel data."""
    matches = {}
    for sheet_name, df, column in [("Lijst", lijst_df, "Objecttype"),
                                   ("Overzicht Kasten", kasten_df, "Kastnaam"),
                                   ("LS Tabbladen", tabbladen_df, "Objecttype")]:
        best_match, score = find_best_match(extracted_text, df, column)
        matches[sheet_name] = (best_match, score)
    return matches

# Example Usage
image_path = r"D:\GameJam\Electrical_Symbol_Recognition\Files\test_image_for_recognition.jpg"
extracted_text = extract_text_from_image(image_path)
matches = compare_with_excel(extracted_text)

print("Extracted Text:", extracted_text)
print("Matches:", matches)
