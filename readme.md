
DownPlayer  
===================  
  
A simple music downloader and player build with Python. <br />  
  
  
Contents :  
 1. [What is it](#what-is-it)  
 2. [Requirements](#requirements)  
 4. [Usage](#usage)  
 5. [Note](#note)  
   
  
----------  
  
What is it  
--------  
  
>**DownPlayer** is a simple music downloader and player built using python's tkinter. The interface is very simple (just a few buttons, entry to give song / artist name). This was made just to test some api working of Youtube Data API v3. <br />  
  
----------  
  
    
Requirements  
------------  
  
#### For Windows / Linux:   
- Python 3 and above should be installed on the system.  
- Run this command in the terminal / cmd:  
```  
pip install requirements.txt  
```  
- [youtube-dl](https://github.com/ytdl-org/youtube-dl) is being used to download the songs. It uses ffmpeg to convert the downloaded song to mp3 extension. Make sure [ffmpeg](https://ffmpeg.org/) is installed on the system. It will be used for conversions among song formats. (Works best with Linux systems)   
- Youtube Data API v3 is used to get the search results. Make sure you have the key to access it and just insert it in the main.py file. (for api_key placeholder)  
- You are good to go.  
  
  
Usage  
------------------  
- Once the dependencies are installed, just run the following code to start the tkinter application:  
```  
python main.py  
```  
- After that, the interface is pretty elementary to work on.  
- Just enter the name of song / artist and after the download is complete, you can simply browse the file through the app and can play the song. (All downloaded songs will be converted to mp3, given that ffmpeg is working fine!)  
- You can also bundle the code using pyinstaller and make an executable which is portable. Just run the following command in the terminal:  
```  
pyinstaller.exe --onefile --icon=your_app_icon.ico main.py  
```  
___________________  
  
Note  
--------------------  
This elementary app was made just to test some stuff, illegal downloading of songs should be avoided. The code is distributed under the **MIT License.**  
_______________