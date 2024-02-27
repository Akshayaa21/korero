import { useState } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  const createBlobUrl = (data: any) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);

    // Append recorded message to messages
    const myMessage = { sender: "me", blobUrl };
    const messagesArr = [...messages, myMessage];

    // Convert blob url to blob object
    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        // Construct Audio to send file
        const formData = new FormData();
        formData.append("file", blob, "myFile.wav");

        // Send from data to API endpoint
        await axios
          .post("http://localhost:8000/post-audio", formData, {
            headers: { "Content-Type": "audio/mpeg" },
            responseType: "arraybuffer",
          })
          .then((res: any) => {
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBlobUrl(blob);

            // Append to audio
            const hannahMessage = { sender: "hannah", blobUrl: audio.src };
            messagesArr.push(hannahMessage);
            setMessages(messagesArr);

            setIsLoading(false);
            audio.play();
          })
          .catch((err) => {
            console.error(err.message);
            setIsLoading(false);
          });
      });
  };

  return (
    <div className="h-screen overflow-y-hidden">
      <div style={{background: '#FFFFFF'}}>
        <Title setMessages={setMessages} />
        <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        
        {/* Conversation */}
        <div className="mt-5 px-20">
          {messages.map((audio, index) => {
            return (
              <div
                key={index + audio.sender}
                className={
                  "flex flex-col " +
                  (audio.sender == "hannah" && "flex items-end")
                }
              >
                {/* Sender */}
                <div className="mt-4">
                  <p className={
                    audio.sender == "hannah" 
                       ? "text-right mr-2 italic text-gray-800"
                       : "ml-2 italic text-gray-800"}
                  >
                    {audio.sender}
                  </p>
                     {/* AudioMessage*/}
                  <audio 
                      src={audio.blobUrl}
                      className="appearance-none"
                      controls
                  />  
                </div>
              </div>
            );
          })}
        </div>
        {messages.length == 0 && !isLoading &&(
          <div className="text-center font-light italic mt-40">
             Welcome to Korero. Hannah is your Interview Practice Assistant. Send Hannah a message...
          </div>
        )}

       {isLoading &&(
          <div className="text-center font-light italic text-black mt-40 animate-pulse">
             Gimme a few seconds...
          </div>
       )}

        {/* Recorder */}
        <div className="fixed bottom-0 w-full py-1 border-t text-center" style={{background: '#3AAFA9'}}>
          <div className="flex justify-center items-center w-full">
            <RecordMessage handleStop={handleStop} />
          </div>
        </div>
       </div>
      </div>
    </div>
  );
}

export default Controller;
