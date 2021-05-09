import time
from glob import glob
import os
import logging

import cv2
import pdf2image
from PIL import Image
import numpy as np


def pdf2jpg(file_name):
    DPI = 200
    FIRST_PAGE = None
    LAST_PAGE = None
    FORMAT = 'jpg'
    THREAD_COUNT = 1
    USERPWD = None
    USE_CROPBOX = False
    STRICT = False
    #Windows
    pil_images = pdf2image.convert_from_path(file_name,poppler_path=r'C:\poppler-0.68.0_x86\poppler-0.68.0\bin', dpi=DPI, first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD, use_cropbox=USE_CROPBOX, strict=STRICT)
    
    #Linux
    #pil_images = pdf2image.convert_from_path(file_name,poppler_path='/usr/bin', dpi=DPI, first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD, use_cropbox=USE_CROPBOX, strict=STRICT)
    return pil_images

def convert_to_jpg(file_name,target_file_path):

    if file_name.lower().endswith(('.png', '.jpeg', '.bmp','.jpg')):

        img = Image.open(file_name)
        logging.info('Image Info:')
        logging.info(img.format)
        logging.info(img.size)
        logging.info(img.mode)
        #target_file_name = '.'.join(file_name.split('.')[:-1]) + '.jpg'
        target_file_name = '.'.join(target_file_path.split('.')[:-1]) + '.jpg'
        cv2.imwrite(target_file_name, np.asarray(img))
        logging.info("Successfully converted image to JPG "+ target_file_name)
        #os.remove(file_name)
        #return target_file_name
        
     
   
    elif file_name.lower().endswith(('.pdf')):
        pdf_image = pdf2jpg(file_name)
         
        for i, image in enumerate(pdf_image):
            target_file_name = '.'.join(target_file_path.split('.')[:-1]) + '_page_' + str(i) + '.jpg'
            #target_file_name = '.'.join(target_file_path.split('.')[:-1]) + '.jpg'
            image.save(target_file_name)
             
       
    else:
        logging.info(f'Unknown file format:{file_name}')
     
        
        
def convert_all_files(input_images_folder_path,processed_images_path):
    start_time = time.time()
    #logging.info(input_images_folder_path)
          
    img_path = input_images_folder_path+ "/*.*"        
    img_names = glob(img_path)
    for filename in img_names:
        #logging.info(filename)
        target_file_path = processed_images_path+"/"+os.path.basename(filename)
        #logging.info(target_file_path)
        try:
            convert_to_jpg(filename,target_file_path) 
        except Exception as e:
            pass
            logging.info(f'Failed in convert_to_jpg at:{str(e)}'  )
        
    logging.info("Time taken to convert "+ str(len(img_names))+"  files to jpg files: "+str(((time.time() - start_time)/60))+" minutes") 
    