## **AlwaysHere**

### **Overview**  
**AlwaysHere** is a platform that allows you to connect with AI-powered versions of your friends and loved ones when they're unavailable. This conversational AI simulates a person's communication style and tone, creating a deeply personal and engaging experience. Whether it's lighthearted banter, meaningful conversations, or simply lending an ear, **AlwaysHere** ensures that you're **always connected**. 

---
### **Note**
- Currently the config.py gives the sys-prompt to the Llama 3.1-8b model to act like me so please edit the config.py for the same. I am currently working on extending this project to a much open-source project(as long as I am not hindered by computing power and voices by ElevenLabs)
- I worked on this project for the FractalTech hackathon and was built over the span of a 5-6 hours, so this is a very rudimentary implementation of the same. 
---

### **Features**

- 🎤 **AI Conversations**: Speak to the AI version of your friends with real-time voice recording, transcription, and AI-generated responses.
- 🗣️ **Natural Voice Responses**: Responses are converted to lifelike audio using ElevenLabs, ensuring conversations feel warm and personal.
- 📄 **Transcript Generation**: Get a concise transcript of the entire conversation for reference.
- 📧 **Email Updates**: Automatically send a summary of the conversation and stitched user voice recordings to the actual friend.
- ✅ **End Chat Safely**: Clean up sessions and temporary files with a simple "End Chat" button.
- 🖥️ **User-Friendly Interface**: Minimalistic UI inspired by modern conversational tools, offering a seamless user experience.

---

### **Tech Stack**

| **Technology**   | **Purpose**                                 |
|------------------|---------------------------------------------|
| **Flask**        | Backend server for handling requests        |
| **Cerebras**     | AI model inference for generating responses |
| **ElevenLabs**   | Realistic text-to-speech voice generation   |
| **Deepgram**     | Audio transcription (speech-to-text)        |
| **HTML/CSS/JS**  | Frontend development                        |
| **Bootstrap**    | Modern and responsive UI design             |

---

### **How It Works**

1. **Start a Conversation**:  
   - Visit the app's home page and click "Start Conversation."
2. **Speak to the AI**:  
   - Use the microphone button to record your message.  
   - Deepgram transcribes your audio into text.
3. **AI Responds**:  
   - The transcribed text is sent to Cerebras' AI, which generates a natural response.  
   - ElevenLabs converts the response into lifelike audio.
4. **Seamless Experience**:  
   - Listen to the AI's reply, view the chat history, and continue the conversation.
5. **End Chat & Update**:  
   - Upon ending the conversation, a concise transcript and user-stitched audio can be sent via email to keep both parties updated.

---

### **Setup Instructions**

#### Prerequisites  
- **Python 3.9+**
- **pip** (Python package installer)
- API Keys for:
  - [Cerebras](https://cerebras.net/)
  - [ElevenLabs](https://elevenlabs.io/)
  - [Deepgram](https://deepgram.com/)

#### Steps to Run Locally

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/varun1352/AlwaysHere.git
   cd AlwaysHere/backend
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:  
   Create a `.env` file in the root directory and add the following keys:

   ```plaintext
   CEREBRAS_API_KEY=your_cerebras_api_key
   ELEVEN_LABS_API_KEY=your_elevenlabs_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   ELEVENLABS_VOICE_ID=your_voice_id
   FLASK_ENV=development
   ```

5. **Run the App**:

   ```bash
   python app.py
   ```

6. **Access the App**:  
   Visit `http://127.0.0.1:5000` in your browser.

---

### **Project Structure**

```
AlwaysHere/
│
├── backend/
│   ├── app.py                 # Flask application
│   ├── config.py              # System prompt and configuration
│   ├── static/                # Static assets (CSS, JS, audio)
│   │   ├── css/
│   │   ├── js/
│   │   └── audio/
│   ├── templates/             # HTML templates
│   ├── requirements.txt       # Dependencies
│   └── .env                   # Environment variables (ignored)
│
└── README.md                  # Project documentation
```

---

### **Planned Features**
1. **User Authentication**: Create accounts and manage profiles with secure logins.
2. **Networking & Friend Requests**: Connect with friends and manage AI agents.
3. **AI Relationship Memory**: Enhance prompts to simulate unique relationships.
4. **Profile Management**: Allow users to create and update their AI versions.
5. **Improved UI/UX**: Sleek, interactive design for an immersive experience.

---

### **Contributing**
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

### **License**
This project is licensed under the [MIT License](LICENSE).

---

### **Acknowledgments**
- [Cerebras Cloud](https://cerebras.net/)
- [ElevenLabs](https://elevenlabs.io/)
- [Deepgram](https://deepgram.com/)

---

### **Contact**
For any questions or feedback, feel free to reach out:
- **Name**: Varun  
- **Email**: your-email@example.com  
- **Portfolio**: [varun1352.github.io](https://varun1352.github.io/)  

