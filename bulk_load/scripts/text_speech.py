import time
from glob import glob
import os
import logging

import PyPDF2 
import pyttsx3




def convert_text_to_speech(filename,output_dir_path,ocr_files_path):
    start_time = time.time()
    
    file_number=0    
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    #print (rate) 
    engine.setProperty('rate', 140)
         
       
    text_files = ocr_files_path+'/*'
    text_files = glob(text_files)
    #logging.info(text_files)
    
    try:
        file_number+=1
        #logging.info(f'Processing file:{file_number}'+os.path.basename(filename))
        for filename in text_files:
            #logging.info(filename)
            pre, ext = os.path.splitext(os.path.basename(filename))
            audio_filename = output_dir_path+'/'+pre+'.mp3' 
            text_file = open(filename, "r+",encoding='utf-8')
            text = text_file.read()
            #logging.info(audio_filename)
            engine.save_to_file(text, audio_filename)
            engine.runAndWait()
            text_file.close()   
    except Exception as e:
        pass
        logging.info("Failed in convert_text_to_speech at: " + str(e))
        
              
    logging.info("Time taken to convert "+ str(1)+" text files to mp3 files: "+str(((time.time() - start_time)/60))+" minutes") 
    return audio_filename

def convert_pdf_to_speech(filename,output_dir_path):
    start_time = time.time()    
       
    engine = pyttsx3.init()
    audio_filename = ""  
             
            
    #logging.info(filename)
    pre, ext = os.path.splitext(os.path.basename(filename))
    audio_filename = output_dir_path+'/'+pre+'.mp3' 
    
    # creating a pdf file object 
    pdfFileObj = open(filename, 'rb') 
        
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        
    # printing number of pages in pdf file 
    #print(pdfReader.numPages) 
    text = ""
    for i in range(pdfReader.numPages-1):
        
        # creating a page object 
        pageObj = pdfReader.getPage(i) 
        
        # extracting text from page 
        text = text+ pageObj.extractText()
        
    # closing the pdf file object 
    pdfFileObj.close() 
    #logging.info(audio_filename)
    #print(text)
    if not text:
        return ""
    engine.save_to_file(text, audio_filename)
    engine.runAndWait()
              
  
    
          
    #logging.info("Time taken to convert "+ str(1)+" pdf files to mp3 files: "+str(((time.time() - start_time)/60))+" minutes") 
    return audio_filename