// Select the button
const speakButton = document.getElementById('buttonNormal');

// Add a click event listener to the button
speakButton.addEventListener('click', () => {
  // Create a new speech utterance
  const utterance = new SpeechSynthesisUtterance("Helloooo");

  // Customize speech properties (optional)
  utterance.pitch = 1.0; // Pitch (0.1 to 2.0)
  utterance.rate = 1.0;  // Speed (0.1 to 10.0)
  utterance.lang = 'en-US'; // Language (e.g., 'en-US' for English)

  // Speak the utterance
  speechSynthesis.speak(utterance);
});
