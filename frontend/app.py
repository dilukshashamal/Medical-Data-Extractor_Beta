import streamlit as st
import requests
import fitz
import ast
import time
import os
import uuid

URL = "http://127.0.0.1:8000/extract_from_doc"

st.title("IDP Medical Data Extractor 👩‍⚕️")

# File uploader for PDFs
file = st.file_uploader("Upload file", type="pdf")

# Radio button for selecting document type
col3, col4 = st.columns(2)
with col3:
    file_format = st.radio(
        label="Select type of document",
        options=["prescription", "patient_details"],
        horizontal=True
    )

# Button to process file and send data
with col4:
    if file and st.button("Upload PDF", type="primary"):
        st.session_state.clear()
        bar = st.progress(50)
        time.sleep(3)  
        bar.progress(100)
        
        # Save uploaded PDF to a temporary local file
        temp_file_path = f"temp_{uuid.uuid4()}.pdf"
        with open(temp_file_path, "wb") as f:
            f.write(file.getvalue())

        # Prepare API request
        payload = {'file_format': file_format}
        try:
            with open(temp_file_path, 'rb') as temp_file:
                files = [('file', temp_file)]
                headers = {}

                # Send file to backend API
                response = requests.post(URL, headers=headers, data=payload, files=files)
                response.raise_for_status()
                dict_str = response.content.decode("UTF-8")
                data = ast.literal_eval(dict_str)
                st.session_state.data = data

        except Exception as e:
            st.error(f"Error occurred: {e}")
        finally:
            time.sleep(1)  # Wait before removing the file to ensure it's no longer in use
            os.remove(temp_file_path)  # Clean up temporary file

# Display the PDF and extracted details
if file:
    # Convert PDF to images using PyMuPDF
    def pdf_to_images(pdf_file):
        images = []
        with fitz.open(stream=pdf_file.getvalue(), filetype="pdf") as pdf_document:
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                pix = page.get_pixmap(dpi=300)
                img = pix.tobytes("png")  
                images.append(img)
        return images

    pages = pdf_to_images(file)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your File")
        st.image(pages[0], use_container_width=True)  # Updated to use 'use_container_width'

    with col2:
        if "data" in st.session_state:
            st.subheader("Details")
            if file_format == "prescription":
                name = st.text_input(label="Name", value=st.session_state.data.get("patient_name", ""))
                address = st.text_input(label="Address", value=st.session_state.data.get("patient_address", ""))
                medicines = st.text_input(label="Medicines", value=st.session_state.data.get("medicines", ""))
                directions = st.text_input(label="Directions", value=st.session_state.data.get("directions", ""))
                refill = st.text_input(label="Refill", value=st.session_state.data.get("refill", ""))
            elif file_format == "patient_details":
                name = st.text_input(label="Name", value=st.session_state.data.get("patient_name", ""))
                phone = st.text_input(label="Phone No.", value=st.session_state.data.get("phone_no", ""))
                vacc_status = st.text_input(
                    label="vaccination status",
                    value=st.session_state.data.get("vaccination_status", "")
                )
                med_problems = st.text_input(
                    label="Medical Problems", value=st.session_state.data.get("medical_problems", "")
                )
                has_insurance = st.text_input(
                    label="Insurance", value=st.session_state.data.get("has_insurance", "")
                )
            if st.button(label="Submit", type="primary"):
                st.success("Details successfully recorded.")
                st.session_state.clear()
