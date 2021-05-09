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
 
  

 
  


def convert_jpg_to_text(input_images_folder_path,filename,ocr_files_path,ocr_engine_list):
    start_time = time.time()
     

    img_path = input_images_folder_path+'/*'
    img_names = glob(img_path)
    file_number=0 
    complete_text = ""
    

    
    for ocr_engine in ocr_engine_list:
        #text_filename = ocr_files_path+'/'+os.path.basename(filename).replace('.tiff','.txt')
        pre, ext = os.path.splitext(os.path.basename(filename))
        text_filename = ocr_files_path+'/'+ocr_engine+'/'+pre+'.txt'    
        text_file = open(text_filename, "w+",encoding='utf-8')
        for filename in img_names:
            try:
                file_number+=1
                #logging.info(f'Processing file:{file_number}'+os.path.basename(filename))
         
    
                if ocr_engine in 'Tesseract':
                    #logging.info('using Tesseract OCR')
                    text = ocr_tesseract(filename)
        
                    complete_text = complete_text + text         
            except Exception as e:
                pass
                logging.info("Failed in convert_jpg_to_text at: " + str(e))
        text_file.write("%s" % complete_text)
        text_file.close()        
    logging.info("Time taken to convert "+ str(len(img_names))+" jpg files to text files: "+str(((time.time() - start_time)/60))+" minutes") 

