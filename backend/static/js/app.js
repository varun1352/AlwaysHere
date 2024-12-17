let isRecording = false;
let mediaRecorder;
let audioChunks = [];

function toggleRecording() {
    const micButton = document.getElementById("mic-button");

    if (!isRecording) {
        startRecording();
        micButton.textContent = "⏹ Stop Recording";
    } else {
        stopRecording();
        micButton.textContent = "🎤 Start Recording";
    }
    isRecording = !isRecording;
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.start();
        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        console.log("Recording started...");
    } catch (error) {
        console.error("Error accessing microphone:", error);
        alert("Could not access microphone. Please check permissions.");
    }
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();

        mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            sendAudio(audioBlob);
        });
        console.log("Recording stopped.");
    }
}

async function sendAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob);

    try {
        const response = await fetch("/api/message", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        updateChat(data.user_message, data.ai_response, data.audio_url);
    } catch (error) {
        console.error("Error sending audio:", error);
        alert("Something went wrong. Please try again.");
    }
}

function updateChat(userMessage, aiMessage, audioUrl) {
    const chatBox = document.getElementById("chat-box");

    // Append user message (aligned to right)
    const userDiv = document.createElement("div");
    userDiv.className = "flex justify-end";
    userDiv.innerHTML = `
        <div class="bg-blue-500 text-white p-3 rounded-lg max-w-xs">
            ${userMessage}
        </div>
    `;
    chatBox.appendChild(userDiv);

    // Append AI message (aligned to left)
    const aiDiv = document.createElement("div");
    aiDiv.className = "flex items-start";
    aiDiv.innerHTML = `
        <div class="bg-gray-200 text-gray-800 p-3 rounded-lg max-w-xs">
            ${aiMessage}
        </div>
    `;
    chatBox.appendChild(aiDiv);

    // Auto-scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Play AI voice response immediately
    const audio = new Audio(audioUrl);
    audio.play().catch(error => console.error("Error playing audio:", error));
}



function endChat() {
    const sendTranscript = document.getElementById("send-transcript").checked;

    const formData = new FormData();
    formData.append("send_transcript", sendTranscript);

    fetch('/api/end-chat', {
        method: 'POST',
        body: formData
    })
    .then(() => {
        window.location.href = '/';
    })
    .catch(err => console.error("Error ending chat:", err));
}


