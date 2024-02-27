import json
import random 

#get recent messages
def get_recent_messages():

    #define the file name and learn instruction 
    file_name = "stored_data.json"
    learn_instruction = {
        "role":"system",
        "content":"You are interviewing the user for a back-end Python developer entry level position.Ask short questions that are relevant to a junior Python level developer. Your name is Hannah. The user is Shaya.Keep your answers to under 30 words."
    }

    #initialize messages 
    messages = []

    # add a random element 
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some dry humour."
    else:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include a rather challenging question."

    messages.append(learn_instruction)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            #append last 5 items of data 
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
            
                else:
                  for item in data[-5:]:
                    messages.append(item)
    
    except Exception as e:
        print(e)
        pass

    return messages 

# Store messages
def store_messages(request_message, response_message):

   # Define the file name
    file_name = "stored_data.json"

    # Get recent messages
    messages = get_recent_messages()[1:]

    # Add messages to db
    user_message = {"role": "user","content":request_message}
    assistant_message = {"role":"assistant", "content":response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file 
    with open(file_name, "w") as f:
        json.dump(messages, f) 


# Reset messages
def reset_messages():
    # overwrite current file with nothing
    open("stored_data.json", "w")