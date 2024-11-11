# transcricao_video.py
import os
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Função para extrair o áudio do vídeo
def extrair_audio(video_path, audio_output):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output)
    print(f"Áudio extraído e salvo como: {audio_output}")

# Função para dividir o áudio em partes com base no silêncio
def dividir_audio(audio_path):
    sound = AudioSegment.from_wav(audio_path)

    # Dividir o áudio com base no silêncio
    chunks = split_on_silence(
        sound,
        min_silence_len=500,  # Mínimo de 500ms de silêncio para detectar uma pausa
        silence_thresh=sound.dBFS - 14  # Limite de silêncio
    )
    
    print(f"Áudio dividido em {len(chunks)} partes.")
    return chunks

# Função para transcrever o áudio e salvar em um arquivo .txt
def transcrever_audio(chunks, arquivo_saida):
    recognizer = sr.Recognizer()

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            chunk.export(f"chunk{i}.wav", format="wav")
            with sr.AudioFile(f"chunk{i}.wav") as source:
                audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio, language="pt-BR")
                    f.write(f"Trecho {i + 1}: {text}\n")
                    print(f"Trecho {i + 1}: {text}")
                except sr.UnknownValueError:
                    f.write(f"Trecho {i + 1}: Não foi possível entender o áudio\n")
                    print(f"Trecho {i + 1}: Não foi possível entender o áudio")
                except sr.RequestError:
                    f.write(f"Trecho {i + 1}: Erro ao processar a requisição\n")
                    print(f"Trecho {i + 1}: Erro ao processar a requisição")

# Função para excluir todos os chunks gerados
def excluir_chunks(chunks):
    for i, chunk in enumerate(chunks):
        os.remove(f"chunk{i}.wav")


# Caminho do vídeo e arquivo de saída de áudio
video_path = "Colabora Enactus - Processo Seletivo (ESALQ USP).mp4"  # Coloque o nome do seu arquivo de vídeo aqui
audio_output = "Colabora Enactus - Processo Seletivo (ESALQ USP).wav"
arquivo_saida = "Colabora Enactus - Processo Seletivo (ESALQ USP).txt"  # Arquivo onde a transcrição será salva

# Extrair o áudio do vídeo
extrair_audio(video_path, audio_output)

# Dividir o áudio em trechos menores
audio_chunks = dividir_audio(audio_output)

# Transcrever o áudio e salvar em um arquivo .txt
transcrever_audio(audio_chunks, arquivo_saida)

# Excluir todos os chunks gerados
excluir_chunks(audio_chunks)

print(f"Transcrição salva no arquivo: {arquivo_saida}")
