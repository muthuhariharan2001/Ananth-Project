# utils.py
from PIL import Image
import imagehash
import pytesseract
import cv2
from fuzzywuzzy import fuzz
import re

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Save temp processed image for OCR
    temp_path = image_path.replace(".jpg", "_processed.jpg")
    cv2.imwrite(temp_path, thresh)

    text = pytesseract.image_to_string(Image.open(temp_path))
    return text.strip()

# def compare_text(text1, text2):
#     words1 = set(text1.lower().split())
#     words2 = set(text2.lower().split())
#     common = words1.intersection(words2)
#     if max(len(words1), len(words2)) == 0:
#         return 0
#     return round((len(common) / max(len(words1), len(words2))) * 100, 2)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    return text.strip().lower()

def compare_text(text1, text2):
    text1_clean = clean_text(text1)
    text2_clean = clean_text(text2)
    
    print("Cleaned Uploaded:", repr(text1_clean))
    print("Cleaned DB:", repr(text2_clean))

    return fuzz.token_set_ratio(text1_clean, text2_clean)

def generate_image_hash(image_path):
    with Image.open(image_path) as img:
        return str(imagehash.average_hash(img))
