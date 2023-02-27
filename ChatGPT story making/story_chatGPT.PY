import openai
import speech_recognition as sr 
import pyttsx3
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def Say_voice(Text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id) #0,3, 5, 8, 9
    engine.setProperty('rate', 180)
    print(Text)
    engine.say(Text)
    engine.runAndWait()

def Listen_voice():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)
        # audio = r.listen_in_background(source,callback= 2)

    try:
        print("Recognizing......")
        # query = r.recognize_bing(audio_data= audio,language='en-in',)
        query = r.recognize_google(audio_data= audio,language='en-in')
        print(f"You Said: {query}")
    except Exception as e:
        print(e)
    return query
        
def OpenAI_Response(query):

    output_ = openai.Completion.create(
        # engine = "text-davinci-003",
        model = "text-davinci-003",
        prompt = query,
        temperature = 0.9,
        max_tokens = 1500,
        top_p = 1,
        best_of = 3,
        frequency_penalty = 0.0,
        presence_penalty = 0.6
        # stop = []
    )['choices'][0]['text']
    
    # print(output_)
    return output_

def file_handling(file_name,x=False):

    if file_name == 'child':
        child = open('story_making_kides.txt','r')
        for item in child:
            # print(item)
            file_name1 = OpenAI_Response(item)
            if x== False:
                file_name1 = str(file_name1)

                print(file_name1)
                file_name1="child "+file_name1+"must.txt"
                file_name1.replace('\n','').replace('"must','')
                
                print(file_name1[0])
                file = open(file_name1,'a')
                file.write(file_name1)
                x= True
            else:

                file.write(item)
                file.write(file_name1)



    
    if file_name == 'adult':
        child = open('story_making_adults.txt','r')
        for item in child:
            print(item)





if __name__== "__main__":


    file = input("for child 'c' and adults 'a' enter: ")
    if file == 'c' or file == 'C':
        file_handling('child')
    elif file == 'a' or file == 'A':
        file_handling('adult')

    Say_voice('hello bro')
    # x= Say_voice(Listen_voice())

    # Say_voice(OpenAI_Response("create a title for a storybook for adults love and romance."))

