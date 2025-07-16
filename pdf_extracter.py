from pathlib import Path
import os
import io
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import datetime
import re 
import csv


def check_folder(folder_path):
    folder = Path(folder_path)

    if folder.is_dir():
        return next(folder.iterdir())
    else :
        return False


def number_of_files(folder_path):
    count = 0 
    try:
        for folder_path, _, files in os.walk(folder_path):
            count += len(files)
    except FileNotFoundError:
        print("file not found")
    except Exception as e :
        print("error",e)
    return count

def find_paths_files(folder_path,recursive = False):
    file_paths = []
    folder = Path(folder_path)
    for item in folder.rglob('*'):
        if item.is_file():
            file_paths.append(item)
    return file_paths


def extract_text_old_api():
   
    laparams = LAParams(
        char_margin=2.0,
        line_margin=0.5,
        word_margin=0.1,
        boxes_flow=0.5,
        detect_vertical=True
    )

    rsrcmgr = PDFResourceManager()
    output_string = io.StringIO()
    device = TextConverter(rsrcmgr, output_string, laparams=laparams)
    pdf_path = find_paths_files(folder_path)
    try:
       with open(pdf_path[i], 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp):
                interpreter.process_page(page)
                text = output_string.getvalue()
                return text
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred during PDF extraction: {e}")
        return ""
    finally:
        device.close()
        output_string.close()






folder_path = r"YOUR_FOLDER_PATH"

a = check_folder(folder_path)
if a==0 :
    print("folder empty")
else:
    print ("folder non-empty")

n = number_of_files(folder_path)
print("number of files",n)

paths = find_paths_files(folder_path,recursive = False)
for file in paths:
    print(file)

content = []
for i in range(0,n):
    content.append(extract_text_old_api()) 

curr_date = datetime.date.today()
date_str = curr_date.strftime(r"%d-%m-%y")
filename = f"Extracted_text_{date_str}"
with open(filename,"a+",encoding="utf-8") as f_out: 
    for i in range(len(content)):
        f_out.write(content[i]) 

f_out.close() 


def get_email(documents):
    emails = []
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    for resume_text in documents:
        lines = resume_text.split('\n')
        for line in lines:
            found_emails = email_pattern.findall(line)
            for email in found_emails:
                emails.append(email)

    return emails

def get_mobile(documents):
    mobile = []
    mobile_pattern = re.compile(r'(?:\+\d{1,3}[ -]?)?\d{7,14}')
    for resume_text in documents:
        lines = resume_text.split('\n')
        for line in lines:
            found_mobile = mobile_pattern.findall(line)
            for num in found_mobile:
                
                clean_num = num.replace(' ', '').replace('-', '').replace('.', '')
                
                if len(clean_num) >= 7 and len(clean_num) <= 15: 
                    mobile.append(clean_num)

    return mobile


def get_name(content):
    name_lst = []
    for i in range (len(content)):
        resumes = content[i]
        words = resumes.split('\n')
        name = str(words[0])
        name_lst.append(name)
    return name_lst

mail_info = get_email(content)
mobile_info = get_mobile(content)
name_info = get_name(content)
details = [mail_info,mobile_info,name_info]
print(details)
class Applicant :
    def __init__(self,name,mobile,email):
        self.name = name
        self.mobile = mobile
        self.email = email
    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}, Phone: {self.mobile}"
    
counting = 0
applicants = []
while counting<2:
    for i in range(n):
        applicant = Applicant(details[2][i],details[1][i],details[0][i])
        print(type(applicant))
        applicants.append(applicant)

        counting+=1
    break
print("\nCreated Applicant Objects")
for app in applicants:
        print(app)
print(applicants)

csv_filename = "applicants_data.csv" 

try:
    
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        
        writer.writerow(["Name", "Email", "Mobile"])

       
        for applicant in applicants:
           
            writer.writerow([applicant.name, applicant.email, applicant.mobile])
    
    print(f"\nData successfully written to {csv_filename}")

except IOError as e:
    print(f"Error writing to CSV file {csv_filename}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
