import time
from glob import glob
import os
import logging

from PIL import Image
import pytesseract

def ocr_tesseract(filename):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    img = Image.open(filename)
    text = pytesseract.image_to_string(img)
    return text
 
  

 
  


def convert_jpg_to_text(filename,processed_files_path,ocr_files_path):
    start_time = time.time()
     

    img_path = processed_files_path+'/*'
    img_names = glob(img_path)
    file_number=0 
    complete_text = ""
    

    
  
    pre, ext = os.path.splitext(os.path.basename(filename))
    text_filename = ocr_files_path+'/'+pre+'.txt'    
    text_file = open(text_filename, "w+",encoding='utf-8')
    for filename in img_names:
        try:
            file_number+=1
            #logging.info(f'Processing file:{file_number}'+os.path.basename(filename))
     
    
            text = ocr_tesseract(filename)

            complete_text = complete_text + text         
        except Exception as e:
            pass
            logging.info("Failed in convert_jpg_to_text at: " + str(e))
    text_file.write("%s" % complete_text)
    text_file.close()        
    #logging.info("Time taken to convert "+ str(1)+" jpg files to text files: "+str(((time.time() - start_time)/60))+" minutes") 

