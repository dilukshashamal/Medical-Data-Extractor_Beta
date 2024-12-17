from parser_generic import MedicalDocParser
from utils import parse_with_ner

class PrescriptionParser(MedicalDocParser):
    def parse(self):
        parsed_data = parse_with_ner(self.text)
        return {
            "patient_name": parsed_data.get("patient_name", "Not Found"),
            "patient_address": parsed_data.get("patient_address", "Not Found"),
            "medicines": parsed_data.get("medicines", []),
            "directions": "Not Found",
            "refill": "Not Found"
        }

if __name__ == "__main__":
    sample_text = """
    Name: Marta Sharapova 
    Address: 9 tennis court, DC
    Prednisone 20 mg
    Directions: Take 2 pills daily.
    """
    parser = PrescriptionParser(sample_text)
    print(parser.parse())
