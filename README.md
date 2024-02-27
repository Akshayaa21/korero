Korero -Ai Python interview practice assistant 
===
Korero is a AI voice bot that uses a combination of OpenAI's API and ElevenLabs' API for voice output with the use of Prompt engineering

It is as a platform for people to practice their Python skills before their actual interviews, this acts as a Virtual Python Interviewer and asks Python related questions. We can talk back and forth with the AI and the users can answer questions in natural language and get a realistic human sounding response back with hilarious humour sometimes.

Technical stack
=======
**Backend**:For backend the project uses Python and FastAPI written with Python to connect with open ai api.

**Frontend**: The project uses React/Typescript for the User Interface.

**Some Libraries/Modules used**:  
1. ```random``` - This module is used to get a random dry humour and difficult question in the process.
2. ```StreamingResponse``` -  This fastspi response module is used to send the Audio back to the openai API.
3. ```openai``` - To use whisper model for speech recognition and to get desired response back with prompt engineering.
