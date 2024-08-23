from pdf2image import convert_from_path
import pytesseract
import argparse
import spacy
import pandas as pd
import re


# Model to get NER Info. Using Large model.
nlp_model = spacy.load('en_core_web_lg')

# Regex pattern for id 
id_pattern = r'\b[A-Z]\d{7}[A-Z]\b'

def save_report(data,report):
    """
    Save the data in a csv file
    Args:
    data <list<list>> list of list with the entities information
    report <str> filepath of the csv file
    """
    df = pd.DataFrame(data, columns=["Entity", "Label"])
    df.to_csv(report, index=False)

def extract_phi(extracted_text):
    """
    Extract the Personal Health Information Person and Date Labels. IDs
    are obtained by regex.

    Args:
    extracted_text <str> text to extract information from.

    Return 
    <list<list>> List of list with 2 values (entity text, entity label) 
    """

    # NLP NER MODEL
    doc = nlp_model(extracted_text)
    data = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "DATE"]: 
            text    = ent.text.replace("\n"," ").strip()
            label   = ent.label_
            entity  = [text,label]
            if entity not in data:
                data.append(entity)

    # REGEX
    ids = re.findall(id_pattern, extracted_text)
    for id_ in ids:
        entity  = [id_,"ID"]
        if entity not in data:
            data.append(entity)

    return data
    

def ocr_pdf(file_name):
    """"
    Read the file_name PDF file.

    Args:
    file_name <str> filepath of the PDF file

    Returns
    <str> Text of the PDF file.
    """
    
    # Get pdf pages
    images = convert_from_path(file_name)
    
    # OCR each image/page
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    
    return text

def get_arguments():
    parser = argparse.ArgumentParser(
                    prog='PDF OCR Extraction for PHI data',
                    description='This systems helps toextract PHI data form a PDF.')
    parser.add_argument('--file', type=str, default='sample_file.pdf',
                        help='filepath of the PDF file')
    parser.add_argument('--report', type=str, default='extracted_phi.csv',
                        help='filepath of the extracted phi data as a csv file')
    return parser.parse_args()
    
if __name__ == "__main__":
    # Get the arguments from console
    args = get_arguments()
    # extract text fro mthe PDF file
    extracted_text = ocr_pdf(args.file)
    # Extract Entities and ids.
    data =  extract_phi(extracted_text)    
    # save data to csv
    save_report(data,args.report)


