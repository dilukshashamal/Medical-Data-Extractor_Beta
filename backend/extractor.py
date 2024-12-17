import fitz  # PyMuPDF
import utils
from parser_patient_details import PatientDetailsParser
from parser_prescription import PrescriptionParser

def extract(file_path, file_format):
    # Step 1: Convert PDF to images
    images = utils.pdf_to_images(file_path)
    
    # Step 2: Preprocess and extract text from images
    full_text = ""
    for img in images:
        processed_img = utils.preprocess_image(img)
        text = utils.extract_text(processed_img)
        full_text += f"\n{text}"
    
    # Step 3: Parse data using appropriate parser
    if file_format == "prescription":
        extracted_data = PrescriptionParser(full_text).parse()
    elif file_format == "patient_details":
        extracted_data = PatientDetailsParser(full_text).parse()
    else:
        raise Exception(f"Invalid file format: {file_format}")
    
    return extracted_data

if __name__ == "__main__":
    print(extract("md_1.pdf", "prescription"))
