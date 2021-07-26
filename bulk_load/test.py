# coding: UTF-8
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
#ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0
#ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_KalpanaM
#ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0
 
for voice in voices:
    # to get the info. about various voices in our PC 
    #print("Voice:")
    print("ID: %s" %voice.id)
    #print("Name: %s" %voice.name)
    #print("Age: %s" %voice.age)
    #print("Gender: %s" %voice.gender)
    #print("Languages Known: %s" %voice.languages)
 
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_KalpanaM"
  
# Use female voice
engine.setProperty('voice', voice_id)

#engine.say('I am Sarang')  
engine.say('ई दिल्‍ली, एजेंसियां। लंबे समय से कांग्रेस से नाराज चल रहे  और बढ़ा दी है। सचिन पायलट और मिलिंद')
engine.runAndWait()