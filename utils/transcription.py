import whisper
from pydub import AudioSegment
import os

model = whisper.load_model("base")

def transcribe_audio(file_path):
    # Convert to wav if needed
    if not file_path.endswith(".wav"):
        audio = AudioSegment.from_file(file_path)
        wav_path = os.path.splitext(file_path)[0] + ".wav"
        audio.export(wav_path, format="wav")
        file_path = wav_path

    result = model.transcribe(file_path, word_timestamps=False)
    return result['text'], result['segments']
