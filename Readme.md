# audio_books

## About  
This is a project developed to create audio book from book in any format(pdf,jpg etc.) 
A vision started with helping blind people to listen to any book.  
However,applications are not limited to books only. Any image(even with bad quality) with text can be converted to audio.
 

## Installation
Development Environment used to create this project:  
Operating System: Windows 10 Home  

### Softwares
Anaconda:4.8.5 (https://docs.anaconda.com/anaconda/install/windows/)    
Tesseract:5.0.0 (https://github.com/UB-Mannheim/tesseract/wiki)   
poppler:0.68 (http://blog.alivate.com.au/poppler-windows/)

### Python libraries:
Go to location of environment.yml file and run:  
```
conda env create -f environment.yml
```
## Flow and Design
The basic idea is to convert text to speech.  
Text can be direct text(digital) or images containing text.

How to get text from file:  
1.digital pdf - pypdf2 library  
2.scanned image - Tesseract OCR  

How to convert text to speech:
pytts library

Flow:  
1.Any file(pdf,png,jpg,jpeg,bmp,txt,doc,docx) containing English text.  
2.If pdf is digital  then use pypdf2 to get text else go to step 3  
3.if any other than digital pdf then use image processing pipeline- convert image,clean image, OCR  
4.pytts for speech creation  

## Usage
There are two ways to use this project:
1.Bulk Load
2.Web Application
### Bulk Load
1. Go inside 'bulk_load' folder on command line.  
2. Place files which need to be converted to audio books inside 'input_files' folder  
3. Run:
  ``` 
      conda activate audio_books  
      python main.py       
  ```
4. Get audio files under 'output' folder.  
5. Check for logs under 'logs' folder for any error  
 
### Web Application
1. Go inside 'webapp' folder on command line.
2. Run:
  ``` 
      conda activate audio_books  
      python main.py       
  ```
3. Open 'http://localhost:5000/' in a browser.
4. Upload a file which needs to be converted to audio.
5. Download a audio file.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Next Steps
1. Fix file download issue in web application
2. Check feasibility for other languages than English.

## License


NOTE: This software depends on other packages that may be licensed under different open source licenses.