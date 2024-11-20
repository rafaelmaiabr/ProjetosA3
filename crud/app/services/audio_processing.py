import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def dividir_audio(audio_path):
    sound = AudioSegment.from_wav(audio_path)
    chunks = split_on_silence(
        sound,
        min_silence_len=500,
        silence_thresh=sound.dBFS - 14
    )
    return chunks

def transcrever_audio(chunks, arquivo_saida):
    recognizer = sr.Recognizer()
    transcription_results = []

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            chunk.export(f"chunk{i}.wav", format="wav")
            with sr.AudioFile(f"chunk{i}.wav") as source:
                audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio, language="pt-BR")
                    transcription_results.append(text)
                    f.write(f"Trecho {i + 1}: {text}\n")
                except sr.UnknownValueError:
                    transcription_results.append("Inaudível")
                    f.write(f"Trecho {i + 1}: Inaudível\n")
                except sr.RequestError:
                    transcription_results.append("Erro de requisição")
                    f.write(f"Trecho {i + 1}: Erro de requisição\n")
    return transcription_results
