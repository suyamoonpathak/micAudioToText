const toggleButton = document.getElementById("toggleButton");
const buttonText = document.getElementById("buttonText");
const resultsDiv = document.getElementById("results");

let mediaRecorder;
let audioChunks = [];
let isRecording = false;

async function toggleRecording() {
  if (!isRecording) {
    buttonText.textContent = "Loading..."; // Show loading message
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.start();

      mediaRecorder.onstart = () => {
        audioChunks = [];
        isRecording = true;
        buttonText.textContent = "Stop Recording";
      };

      mediaRecorder.onstop = async () => {
        isRecording = false;
        const blob = new Blob(audioChunks, { type: "audio/wav" });

        const formData = new FormData();
        formData.append("audio", blob, "recording.wav");

        const response = await fetch("/convert", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        resultsDiv.innerHTML = `<p>Text: ${data.message}</p>`;
        buttonText.textContent = "Start Recording"; // Reset button text
      };
    } catch (error) {
      console.error("Error accessing microphone:", error);
      buttonText.textContent = "Start Recording"; // Reset button text
    }
  } else {
    // Handle stopping action
    if (mediaRecorder) {
      mediaRecorder.stop();
    }
    isRecording = false;
    buttonText.textContent = "Start Recording"; // Reset button text
  }
}

toggleButton.addEventListener("click", toggleRecording);
