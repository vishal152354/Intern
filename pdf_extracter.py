import io
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pathlib import Path

def extract_text_old_api(pdf_path):
   
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

    try:
        with open(pdf_path, 'rb') as fp:
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

def check_folder(folder_path):
    folder = Path(folder_path)

    if folder.is_dir():
        return next(folder.iterdir())
    else :
        return False


if __name__ == "__main__":

    
    n = int(input("No of resumes"))
    for i in range(0,n):
        pdf_file_path = input("enter resume pdf path")
        filename = f"extracted_text_{i+1}"
        extracted_content = extract_text_old_api(pdf_file_path) 
        if extracted_content:
            print(f"Text extracted successfully (length: {len(extracted_content)} characters).")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f_out:
                f_out.write(extracted_content)
            print(f"Extracted text saved to: {output_txt_file_path}")
        except Exception as e:
            print(f"Error saving extracted text to file: {e}")
        

        print("\n--- First 500 characters of extracted text ---")
        print(extracted_content[:500])
        if len(extracted_content) > 500:
            print("...")
        else:
            print("No text was extracted.")