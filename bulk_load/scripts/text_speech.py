import time
from glob import glob
import os
import logging

import PyPDF2 
import pyttsx3
import slate3k as slate
from scripts import configuration as config




def convert_text_to_speech(filename,output_dir_path,ocr_files_path):
    start_time = time.time()
    
    file_number=0    
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    #print (rate) 
    engine.setProperty('rate', 140)
    engine.setProperty('voice',config.AUDIO_ID)     
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
            text_file = open(filename, "r+",encoding='utf-8',errors='ignore')
            text = text_file.read()
            #logging.info(audio_filename)
            engine.save_to_file(text, audio_filename)
            engine.runAndWait()
            text_file.close()   
    except Exception as e:
        pass
        logging.info("Failed in convert_text_to_speech at: " + str(e))
        
              
    #logging.info("Time taken to convert "+ str(1)+" text files to mp3 files: "+str(((time.time() - start_time)/60))+" minutes") 
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
    #logging.info(text)
    engine.save_to_file(text, audio_filename)
    engine.runAndWait()
              
  
    
          
    #logging.info("Time taken to convert "+ str(1)+" pdf files to mp3 files: "+str(((time.time() - start_time)/60))+" minutes") 
    return audio_filename

def convert_pdf_to_speech_slate(filename,output_dir_path):
    start_time = time.time()    
       
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    #print (rate) 
    engine.setProperty('rate', 140)
    engine.setProperty('voice',config.AUDIO_ID)  
    audio_filename = ""  
            
    #logging.info(filename)
    pre, ext = os.path.splitext(os.path.basename(filename))
    audio_filename = output_dir_path+'/'+pre+'.mp3' 
    
    with open(filename,'rb') as f:
        complete_text = slate.PDF(f)

    text = ""
    for i,page_text in enumerate(complete_text):
        # extracting text from page 
        #text = text+ page_text 
        #logging.info(f'page_no:{i}')
        #logging.info(page_text)
        engine.save_to_file(page_text,  output_dir_path+'/'+pre+'_page_'+str(i+1)+'.mp3' ) 
        engine.runAndWait() 
   
    #print(type(text))
    #if not text:
     #   return ""
    #logging.info(text)
    #engine.save_to_file(text, audio_filename)
    #engine.runAndWait()
              
          
    #logging.info("Time taken to convert "+ str(1)+" pdf files to mp3 files: "+str(((time.time() - start_time)/60))+" minutes") 
    return audio_filename