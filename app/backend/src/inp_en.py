import whisper
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

model = whisper.load_model("base")

def stt(input_audio):
    result = model.transcribe(input_audio)
    result = result['text']
    return result