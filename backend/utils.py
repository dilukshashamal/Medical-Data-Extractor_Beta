import fitz  # PyMuPDF
import numpy as np
import cv2
from paddleocr import PaddleOCR
from transformers import pipeline

# Initialize PaddleOCR and NER pipeline
ocr = PaddleOCR(use_angle_cls=True, lang='en')
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

# Convert PDF to images
def pdf_to_images(doc_path):
    doc = fitz.open(doc_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        images.append(img)
    return images

# Preprocess image
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    processed_image = cv2.adaptiveThreshold(
        resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 63, 12
    )
    return processed_image

# Extract text using PaddleOCR
def extract_text(img):
    result = ocr.ocr(img, cls=True)
    return "\n".join([line[1][0] for line in result[0]])

# Parse text using NER
def parse_with_ner(text):
    entities = ner_pipeline(text)
    parsed_data = {}
    for entity in entities:
        label = entity["entity_group"]
        word = entity["word"]
        if label == "PER":
            parsed_data["patient_name"] = word
        elif label == "LOC":
            parsed_data["patient_address"] = word
        elif label == "MISC":
            parsed_data.setdefault("medicines", []).append(word)
    return parsed_data
