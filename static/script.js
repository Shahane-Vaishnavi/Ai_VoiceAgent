let mediaRecorder;
let audioChunks = [];

async function startRecording() {
  document.getElementById("transcription").innerHTML = "";
  document.getElementById("statusMsg").innerHTML = "🎙️ Recording...";
  document.getElementById("startBtn").disabled = true;
  document.getElementById("stopBtn").disabled = false;

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.ondataavailable = (e) => {
    audioChunks.push(e.data);
  };

  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: 'audio/webm' });
    const audioUrl = URL.createObjectURL(blob);
    document.getElementById("echoAudio").src = audioUrl;

    const formData = new FormData();
    formData.append("file", blob, "recording.webm");

    try {
      // ✅ Upload
      document.getElementById("statusMsg").innerHTML = "⬆️ Uploading to backend...";
      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      if (data.status === "success") {
        document.getElementById("statusMsg").innerHTML = `
          <div style="color:green; font-weight:bold;">
            ✅ Upload Successful<br>
            File: <code>${data.name}</code><br>
            Type: ${data.type}<br>
            URL: <a href="${data.url}" target="_blank">${data.url}</a>
          </div>
        `;
      } else {
        document.getElementById("statusMsg").innerHTML = "❌ Upload failed.";
      }

      // 🧠 Transcribe
      document.getElementById("statusMsg").innerHTML += "<p>🧠 Transcribing audio...</p>";
      const transcribeRes = await fetch("http://127.0.0.1:8000/transcribe/file", {
        method: "POST",
        body: formData
      });

      const transcribeData = await transcribeRes.json();
      if (transcribeData.transcription) {
        document.getElementById("transcription").innerHTML = `
          <div style="border:2px solid purple; padding:10px; border-radius:10px; background:#f4eaff;">
            <strong>Transcript:</strong><br>
            <span style="font-size:16px;">${transcribeData.transcription}</span>
          </div>
        `;
      } else {
        document.getElementById("transcription").innerHTML = "❌ No transcription returned.";
      }

    } catch (err) {
      document.getElementById("statusMsg").innerHTML = "❌ Upload or transcription failed.";
      console.error("Error:", err);
    }

    document.getElementById("startBtn").disabled = false;
    document.getElementById("stopBtn").disabled = true;
  };

  mediaRecorder.start();
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

async function generateAudio() {
  const text = document.getElementById("textInput").value;
  
  if (!text.trim()) {
    alert("Please enter some text to generate audio.");
    return;
  }

  try {
    const res = await fetch("/generate-voice/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    
    const data = await res.json();
    if (data.audio_url) {
      document.getElementById("player").src = data.audio_url;
    } else {
      alert("Failed to generate audio. Please try again.");
    }
  } catch (err) {
    console.error("Error generating audio:", err);
    alert("An error occurred while generating audio.");
  }
}

