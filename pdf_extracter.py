from pathlib import Path
import os
import io
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


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






folder_path = r"C:\Users\50054\Desktop\intern-Vishal\data"

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


for i in range(0,n):
    content = extract_text_old_api() 


print(content) 
filename = "Extracted_text"
with open(filename,"a+",encoding="utf-8") as f_out: 
    f_out.write(content) 

f_out.close() 
