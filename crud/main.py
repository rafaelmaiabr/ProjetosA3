from flask import Flask, request, jsonify
import os
import time
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

app = Flask(__name__)

UPLOAD_FOLDER_VIDEO = 'upload/video'
UPLOAD_FOLDER_AUDIO = 'upload/audio'
UPLOAD_FOLDER_TEXT = 'upload/text'
os.makedirs(UPLOAD_FOLDER_AUDIO, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_VIDEO, exist_ok=True)

# CRIA ARQUIVO
@app.route('/upload', methods=['POST'])
def upload_file():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400
  file = request.files['file']
  if file.filename == '':
    return jsonify({'error': 'No selected file'}), 400
  if file:
    filename = file.filename
    ext = filename.rsplit('.', 1)[1].lower()
    timestamp = int(time.time())
    new_filename = f"{request.form['name']}_{timestamp}.{ext}"
    if ext in ['mp3', 'wav']:
      file.save(os.path.join(UPLOAD_FOLDER_AUDIO, new_filename))
    elif ext in ['mp4', 'avi']:
      file.save(os.path.join(UPLOAD_FOLDER_VIDEO, new_filename))
    else:
      return jsonify({'error': 'Unsupported file type'}), 400
    return jsonify({'filename': new_filename}), 201

# LISTA ARQUIVOS
@app.route('/files', methods=['GET'])
def list_files():
  audio_files = os.listdir(UPLOAD_FOLDER_AUDIO)
  video_files = os.listdir(UPLOAD_FOLDER_VIDEO)
  return jsonify({'audio': audio_files, 'video': video_files})

# RENOMEIA ARQUIVO
@app.route('/files/<file_type>/<filename>', methods=['PUT'])
def rename_file(file_type, filename):
  data = request.get_json()
  new_filename = data.get('name')
  
  if not new_filename:
    return jsonify({'error': 'New filename not provided'}), 400

  if file_type == 'audio':
    folder = UPLOAD_FOLDER_AUDIO
  elif file_type == 'video':
    folder = UPLOAD_FOLDER_VIDEO
  else:
    return jsonify({'error': 'Invalid file type'}), 400

  file_path = os.path.join(folder, filename)
  new_file_path = os.path.join(folder, new_filename)
  
  if os.path.exists(file_path):
    os.rename(file_path, new_file_path)
    return jsonify({'message': 'File renamed'}), 200
  else:
    return jsonify({'error': 'File not found'}), 404

# DELETA ARQUIVO
@app.route('/files/<file_type>/<filename>', methods=['DELETE'])
def delete_file(file_type, filename):
  if file_type == 'audio':
    folder = UPLOAD_FOLDER_AUDIO
  elif file_type == 'video':
    folder = UPLOAD_FOLDER_VIDEO
  else:
    return jsonify({'error': 'Invalid file type'}), 400
  file_path = os.path.join(folder, filename)
  if os.path.exists(file_path):
    os.remove(file_path)
    return jsonify({'message': 'File deleted'}), 200
  else:
    return jsonify({'error': 'File not found'}), 404


###### TRANSCRIÇÃO DO AUDIO ######
@app.route('/files/converter', methods=['POST'])
def converter():
  data = request.get_json()
  archive = data.get('archive')

  if not archive:
    return jsonify({'error': 'No archive provided'}), 400
  
  extension = archive.rsplit('.', 1)[1].lower()
  if extension in ['mp3', 'wav', 'wav']:
      archive_path = os.path.join(UPLOAD_FOLDER_AUDIO, archive)
      archiveType = 'audio'
  else:
      archive_path = os.path.join(UPLOAD_FOLDER_VIDEO, archive)
      archiveType = 'video'

  # verifica se o arquivo existe
  if not os.path.exists(archive_path):
    print(f"Arquivo não encontrado: {archive_path}")
    return jsonify({'error': 'File not found'}), 404
  
  if archiveType == 'video':
    video_path = archive_path
    audio_output = os.path.join(UPLOAD_FOLDER_AUDIO, f"{archive.rsplit('.', 1)[0]}.wav")
    extrair_audio(video_path, audio_output)

  if archiveType == 'audio':
    audio_path = archive_path
    audio_chunks = dividir_audio(audio_path)
    arquivo_saida = os.path.join(UPLOAD_FOLDER_TEXT, f"{archive.rsplit('.', 1)[0]}.txt")
    transcrever_audio(audio_chunks, arquivo_saida)
    excluir_chunks(audio_chunks)
    print(f"Transcrição salva no arquivo: {arquivo_saida}")

  return jsonify({'message': 'File converted'}), 200


def extrair_audio(video_path, audio_output):
  video = mp.VideoFileClip(video_path)
  video.audio.write_audiofile(audio_output)
  print(f"Áudio extraído e salvo como: {audio_output}")


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

def excluir_chunks(chunks):
    for i, chunk in enumerate(chunks):
        os.remove(f"chunk{i}.wav")  

if __name__ == '__main__':
  app.run(debug=True)