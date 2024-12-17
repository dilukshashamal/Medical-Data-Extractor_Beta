from parser_generic import MedicalDocParser
from utils import parse_with_ner

class PatientDetailsParser(MedicalDocParser):
    def parse(self):
        parsed_data = parse_with_ner(self.text)
        return {
            "patient_name": parsed_data.get("patient_name", "Not Found"),
            "patient_address": parsed_data.get("patient_address", "Not Found"),
            "medical_problems": parsed_data.get("medical_problems", "N/A"),
            "vaccination_status": "Unknown",
            "phone_no": "Not Found"
        }

if __name__ == "__main__":
    sample_text = "Patient Jerry Lucas lives at 4218 Wheeler Ridge Dr. Medical history: N/A."
    parser = PatientDetailsParser(sample_text)
    print(parser.parse())
