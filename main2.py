import pyaudio
import speech_recognition as sr
from speech_recognition import AudioData
import keyboard
recognizer = sr.Recognizer()
def speak(text):
    print("Computer:", text)
def record_audio(seconds=5):
    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
    except Exception as e:
        print("Microphone error:", e)
        speak("Microphone not working.")
        return None, None, None
    print("🎤 Listening... (Press Q to stop)")
    frames = []
    for _ in range(int(16000 / 1024 * seconds)):
        if keyboard.is_pressed('q'): #to stop the program from running
            print("Ending program")
            return None, None, None
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()
    return b"".join(frames), 16000, width
def transcribe_audio(audio_data, sample_rate, sample_width):
    if audio_data is None:
        return False  # stop loop if key pressed
    audio = AudioData(audio_data, sample_rate, sample_width)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        text_lower = text.lower()
        if "hello" in text_lower:
            response = "Hello! How are you?"
        elif "bye" in text_lower or "stop" in text_lower:
            speak("Goodbye!")
            return False
        else:
            response = "I heard you say " + text
        speak(response)
        return True
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return True
    except sr.RequestError:
        speak("Internet is required.")
        return True
def run():
    speak("Assistant started. Press Q anytime to stop.")
    running = True
    while running:
        if keyboard.is_pressed('q'): #stopping the programq
            print("Program stopped by keyboard.")
            break
        audio_data, sample_rate, sample_width = record_audio()
        running = transcribe_audio(audio_data, sample_rate, sample_width)
if __name__ == "__main__":
    run()