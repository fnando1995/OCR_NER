# OCR NER

## Objective:

Extract the text from a PDF file and redact the personal information (ID, names, dates), and save the result into a CSV.

## Installation:

- Create environment (optional)
- Install tesseract: Follow [link](https://ironsoftware.com/csharp/ocr/blog/ocr-tools/install-tesseract/), [link](https://medium.com/@nothanjack/easy-installation-of-tesseract-ocr-on-debian-12-terminal-walkthrough-13120ec7d98c).
- Install python requirements
```
python -m pip install -r requirements
```
- Install NER model from spacy (other models: en_core_web_sm, en_core_web_md, en_core_web_trf)
```
python -m spacy download en_core_web_lg
```

## Methodology

As methodology, I use tesseract for OCR the PDF file, then the text is processed with a general model from spacy to tag  Named Entities (NER). As "IDs" is not exactly a NAMED ENTITY, a simple REGEX is used for capture the IDs in the text. Finally all information is saved in a csv file with columns ENTITY and LABEL.


## Execution:

```
python extract_phi_data.py --help

usage: PDF OCR Extraction for PHI data [-h] [--file FILE] [--report REPORT]

This systems helps toextract PHI data form a PDF.

options:
  -h, --help       show this help message and exit
  --file FILE      filepath of the PDF file
  --report REPORT  filepath of the extracted phi data as a csv file
```

## Result for sample_file.pdf:
```
Entity,Label
Tan Ah Kow,PERSON
NRIC,PERSON
55 years old,DATE
Tan Ah Moi,PERSON
November 2010,DATE
Tan,PERSON
20 June 2015,DATE
Tan Ah Beng,PERSON
year old,DATE
Ah Beng,PERSON
Ah Beng’s,PERSON
1990,DATE
2005,DATE
April 2010,DATE
15 April 2010,DATE
the years,DATE
the last 5 years,DATE
10 February,DATE
20 June,DATE
Wednesday,DATE
actual day,DATE
Monday,DATE
the day,DATE
Spm,PERSON
50 years old,DATE
55 years,DATE
Lee Kuan Yew,PERSON
the day and date,DATE
20 July 2015,DATE
21 years of age,DATE
S1111111X,ID
```


## Future improvements

- This is an automatic PHI data extractor using general models. Tranning for specific cases could improve accuracy.
- Tesseract is used for OCR, but in some cases like ID S2222222Z is not read well ($2222222Z), thus the regex can't find this ID.
- Further postprocessing for the entities in the models could be performed.
