import openai 

from decouple import config


#importing custom func 
from functions.database import get_recent_messages

#retrive env 
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_API_KEY")


#open ai whisper convert audio to text 
def convert_audio_to_text(audio_file):#pass in the audio file 
    try:
        transcript = openai.Audio.transcribe("whisper-1",audio_file)#transcribe is to convert speech into txt doc
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        print(e)
        return
    
# open AI - chatgpt
    #get resopnse to our message
def get_chat_response(message_input):

    messages = get_recent_messages()
    latest_user_message = {"role":"user", "content":message_input}
    messages.append(latest_user_message)
    print(messages)


    try:
        response =openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        print(e)
        return


