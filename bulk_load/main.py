from glob import glob
import errno
import time
import os
import logging  
 

from scripts.image_conversion import convert_all_files
from scripts.image_cleaning import image_cleaning     
from scripts.ocr_generation import convert_jpg_to_text
from scripts.text_speech import convert_text_to_speech,convert_pdf_to_speech
     
 
from nltk.tokenize import sent_tokenize  
   
    
  
 
 
 

def clean_folder(directory):
    filelist =  os.listdir(directory)
    for f in filelist:
        os.remove(os.path.join(directory, f))

'''def directory_backup(source_directory,dest_directory):
    names = os.listdir(source_directory)
    for name in names:
        srcname = os.path.join(source_directory, name)
        dstname = os.path.join(dest_directory, name)
        shutil.copy(srcname, dstname)'''
 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


 
 
 
 
 
 
logging.basicConfig(filename=APP_ROOT+'/'+'logs/'+'execution_log.log', filemode='a+', format=' [%(filename)s:%(lineno)s:%(funcName)s()]- %(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
 
 

 

input_path = APP_ROOT+'/input_files'      
output_dir_path =  APP_ROOT+'/output'
processed_files_path =  APP_ROOT+'/processed_images'
ocr_files_path =  APP_ROOT+'/OCR'
 

input_path_backup = APP_ROOT+'/client_backup'+'/input_files'      
output_dir_path_backup =  APP_ROOT+'/client_backup'+'/output'
processed_files_path_backup =  APP_ROOT+'/client_backup'+'/processed_images'
ocr_files_path_backup =  APP_ROOT+'/client_backup'+'/OCR'

 


      
 
 
 
def convert_books(): 
   


    #clean_folder(input_path)
    #clean_folder(processed_files_path)
    #clean_folder(ocr_files_path)
    #clean_folder(output_dir_path)

 
    start_time = time.time()      
    

    img_path = input_path+ "/*.*"
    #print(img_path)        
    img_names = glob(img_path)
    for filename in img_names:
        start_time_file = time.time()   
        audio_filename = ""
        ext = os.path.splitext(filename)[1]
        if (ext == ".pdf"):
            audio_filename = convert_pdf_to_speech(filename,output_dir_path)

        if not audio_filename and ext in ['.pdf','.png', '.jpeg', '.bmp','.jpg']:
            convert_all_files(filename,processed_files_path)
            image_cleaning(processed_files_path)
            convert_jpg_to_text(filename,processed_files_path,ocr_files_path)
            audio_filename = convert_text_to_speech(filename,output_dir_path,ocr_files_path)
        elif ext in [".txt",".doc",".docx"]:
            audio_filename = convert_text_to_speech(filename,output_dir_path,input_path)
        
        logging.info("Total time taken for generating final output for "+filename+" : "+str(((time.time() - start_time_file)/60))+" minutes")
        clean_folder(processed_files_path)
        clean_folder(ocr_files_path)
    #clean_folder(input_path)

    logging.info("Total time taken for generating final output for "+str(len(img_names))+" files: "+str(((time.time() - start_time)/60))+" minutes")  

    
    

    #Backup all data
    #directory_backup(input_path+'/'+doc_type,input_path_backup)
    #directory_backup(processed_files_path+'/'+,processed_files_path_backup)
    #directory_backup(ocr_files_path+'/'+ocr_files_path_backup+'/')
   
 
    
if __name__ == '__main__':
   try:
       convert_books()
     
   except Exception as e:
        print("Failed in script at: " + str(e))
        logging.error(str(e))
        
