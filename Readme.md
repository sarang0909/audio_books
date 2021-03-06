# audio_books

## About  
This is a project developed to create audio book from book in any format(pdf,jpg etc.) 
A vision started with helping blind people to listen to any book.  
However,applications are not limited to books only. Any image(even with bad quality) with text can be converted to audio.
 

## Installation
Development Environment used to create this project:  
Operating System: Windows 10 Home  

### Softwares
Anaconda:4.8.5  <a href="https://docs.anaconda.com/anaconda/install/windows/">Anaconda installation</a>   
Tesseract:5.0.0 <a href="https://github.com/UB-Mannheim/tesseract/wiki">Tesseract installation</a>   
    Add tesseract path to environment variable 'PATH' e.g C:\Program Files\Tesseract-OCR   
    Add tessdata by creating new environment variable. e.g TESSDATA_PREFIX = C:\Program Files\Tesseract-OCR\tessdata  
poppler:0.68 <a href="http://blog.alivate.com.au/poppler-windows/">Popplert installation</a>

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
Please create a Pull request for any change. 

## Next Steps
1. Fix file download issue in web application
2. Check feasibility for other languages than English.

## License


NOTE: This software depends on other packages that are licensed under different open source licenses.

## Resources
pyttx  <a href="https://pyttsx3.readthedocs.io/en/latest/">Text to Speech library</a>