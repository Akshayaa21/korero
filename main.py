from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse 
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai 

from functions.openai_requests import convert_audio_to_text,get_chat_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import convert_text_to_speech

#initiate app 
app=FastAPI()

origins=["*"]

#CORS-middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],#all 
    allow_headers=["*"],
)

@app.get("/health")
async def check_health():
    return {"message": "healthy"}


# Reset Messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}

@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
  try:  
    # get saved audio
    #audio_input = open("Record.mp3", "rb")

    # Save file from frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")# the file is gonna come from above uploadfile

    # decoding audio
    message_decoded = convert_audio_to_text(audio_input)

    # Guard: ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode audio")
    
    # get chatgpt response
    chat_response = new_func(message_decoded)

    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")
    

    # Store messages 
    store_messages(message_decoded, chat_response)

    # Converting chat response to audio 
    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response")
    
    # Generator that yields chunks of data
    

    def iterfile():
            yield audio_output

    return StreamingResponse(content=iterfile(), media_type="application/octet-stream")

  
  except HTTPException as e:
        raise e

  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail="Internal Server Error")

def new_func(message_decoded):
    chat_response = get_chat_response(message_decoded)
    return chat_response

 

#post bot 
"""@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):#sending file into fast api

    print("heil hitler")"""