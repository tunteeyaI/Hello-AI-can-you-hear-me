import pyaudio #access the mic and the audio system
import speech_recognition as sr #convert audio to text
from speech_recognition import AudioData #convert the input into a format that sr understands
#function to record audio from mic
def record_audio(seconds=5):
    #interface for the microphone
    p=pyaudio.PyAudio()
    #open an audiostream
    stream=p.open(
        format=pyaudio.paInt16, #16 bit audio
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024 # to store the recorded audio
    )
    print("Recording started...")
    frames=[]#store the audio chunks
    for _ in range(0, int(16000 / 1024 * seconds)):
        frames.append(stream.read(1024)) #read chuncks and store
    print("Recording complete")
    #Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    #get sample with-determine the recording format
    width=p.get_sample_size(pyaudio.paInt16)
    #Terminate PyAudio session
    p.terminate()
    #return the recorded audio
    return b"".join(frames), 16000, width
#function to transcribe the audio
def transcribe_audio(audio_data,sample_rate,sample_width):
    #initialize the recognizer
    recognizer=sr.Recognizer()
    #get the audio data
    audio=AudioData(audio_data,sample_rate,sample_width)
    #convert audio to text
    try:
        text=recognizer.recognize_google(audio)
        print("Transcription:",text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("The recognition service is unavaliable")
#main function
def main():
    audio_data, sample_rate, sample_width = record_audio() #get the recording
    transcribe_audio(audio_data, sample_rate, sample_width) #transcribe the recording
if __name__ == "__main__":
    main()