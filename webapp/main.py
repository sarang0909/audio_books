 
import json
from glob import glob
import errno
import time
import os
 

 
 
 
import logging
 
 
 
from flask import Flask, render_template, request,send_from_directory
import json

from scripts.image_conversion import convert_all_files
from scripts.image_cleaning import image_cleaning     
from scripts.ocr_generation import convert_jpg_to_text
from scripts.text_speech import convert_text_to_speech,convert_pdf_to_speech
     
 
        
'''def generate_pan_output(ocr_files_path,output_dir_path,output_df,ocr_engine):
    #output_df.to_csv()
    start_time = time.time()
    img_path = ocr_files_path+"/*.txt"
    print('ocr_files_path:{}'.format(ocr_files_path))
    img_names = glob(img_path)
    for filename in img_names:
        text_file = open(filename, "r+",encoding='utf-8')
        text = text_file.read()
        print(filename)
        FileName = os.path.basename(filename).replace('.txt','')
        output_df = output_df.append({'FileName' : FileName } , ignore_index=True)
        output_df.loc[output_df['FileName']==FileName, 'PAN Number'] =  getPanNumber(text)
        output_df.loc[output_df['FileName']==FileName, 'Name'] = getPanName(text)
        output_df.loc[output_df['FileName']==FileName, 'BirthDate'] =  getPanBirthDate(text)
        output_df.loc[output_df['FileName']==FileName, 'Father Name'] = getPanFatherName(text)
               
                
   # print(output_df)    
    output_df.to_csv(output_dir_path+'/pan_output_'+ocr_engine+'.csv',index=False)
    
    pan_output_df_backup = pd.read_csv(output_dir_path_backup+'/pan_output_'+ocr_engine+'_backup'+'.csv')
    pan_output_df_backup = pan_output_df_backup.append(output_df, ignore_index=True)
    pan_output_df_backup.to_csv(output_dir_path_backup+'/pan_output_'+ocr_engine+'_backup'+'.csv',index=False)
    
    print("Time taken to generate output from  "+ str(len(img_names))+" ocr files: "+str(((time.time() - start_time)/60))+" minutes")
    return output_df'''
    
  
 
 
 

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


 
app = Flask(__name__) 
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
 
 

#logging.basicConfig(filename=APP_ROOT+'/'+'app.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#logging.basicConfig(filename=APP_ROOT+'/'+'app.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(filename=APP_ROOT+'/'+'execution_log.log', filemode='a+', format=' [%(filename)s:%(lineno)s:%(funcName)s()]- %(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
 
#logHandler = logging.FileHandler(APP_ROOT+'/'+'execution_log.log')
#logHandler.setLevel(logging.INFO)
#app.logger.addHandler(logHandler)
#app.logger.setLevel(logging.INFO) 

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

input_path = APP_ROOT+'/input_files'      
output_dir_path =  APP_ROOT+'/output'
processed_files_path =  APP_ROOT+'/processed_images'
ocr_files_path =  APP_ROOT+'/OCR'
 

input_path_backup = APP_ROOT+'/client_backup'+'/input_files'      
output_dir_path_backup =  APP_ROOT+'/client_backup'+'/output'
processed_files_path_backup =  APP_ROOT+'/client_backup'+'/processed_images'
ocr_files_path_backup =  APP_ROOT+'/client_backup'+'/OCR'

 


      
@app.route('/')
def upload_form():
   return render_template('upload.html')
   
@app.route('/upload/<filename>',methods=['GET','POST'])
def send_image(filename):
    logging.info('Inside send_image') 
 
    
    input_folder = output_dir_path+'/'+"Tesseract"+'/'
  
    
    logging.info(input_folder+filename)
    
    #return send_from_directory(input_folder, filename,as_attachment=True)
    return output_dir_path+'/'+"Tesseract"+'/'+filename
	
@app.route("/upload", methods=['GET', 'POST'])
def upload():
   if request.method == 'POST':      
      
      
      #ocr_engine_list = ['Tesseract','Textract','Azure','Google']
      ocr_engine_list = ['Tesseract']     

      
      
      
      clean_folder(input_path)
      clean_folder(processed_files_path)
      clean_folder(ocr_files_path+'/'+ocr_engine_list[0])
      clean_folder(output_dir_path+'/'+ocr_engine_list[0])
      
      
      
      target = input_path
      
      
      for upload in request.files.getlist("file"):
        #logging.info(upload)
        logging.info(upload.filename+' is the file name')
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        '''if (ext == ".jpg") or (ext == ".png") or (ext == ".tif"):
            logging.info("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")'''
        destination = "/".join([target, filename])
        logging.info("Accept incoming file:"+ filename)
        logging.info("Save it to:"+ destination)
        upload.save(destination)
      
      
      
      start_time = time.time()      
      audio_filename = ""
      if (ext == ".pdf"):
          audio_filename = convert_pdf_to_speech(input_path,output_dir_path,ocr_engine_list[0])
      
      if not audio_filename:
        convert_all_files(input_path,processed_files_path)

        image_cleaning(processed_files_path)
        convert_jpg_to_text(processed_files_path,filename,ocr_files_path,ocr_engine_list)
        audio_filename = convert_text_to_speech(filename,output_dir_path,ocr_files_path,ocr_engine_list)
 
       
            
      logging.info("Total time taken for generating final output: "+str(((time.time() - start_time)/60))+" minutes")  
      
       
       
      
      #Backup all data
      #directory_backup(input_path+'/'+doc_type,input_path_backup+'/'+doc_type)
      #directory_backup(processed_files_path+'/'+doc_type,processed_files_path_backup+'/'+doc_type)
      #directory_backup(ocr_files_path+'/'+ocr_engine_list[0]+'/'+doc_type,ocr_files_path_backup+'/'+ocr_engine_list[0]+'/'+doc_type)
      
      file_name = audio_filename
      logging.info(file_name)
      logging.info(filename)
      return render_template("success.html", name = file_name, file_name= file_name)  
	   
if __name__ == '__main__':
   try:
    #app.run(debug = True)
        app.run(host = "0.0.0.0")
   except Exception as e:
        print("Failed in script at: " + str(e))
        logging.error(str(e))
        
