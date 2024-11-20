import time, os
from flask import request, jsonify
from flask_cors import CORS
from app import app
from app.services.audio_extraction import extrair_audio
from app.services.audio_processing import dividir_audio, transcrever_audio
from app.services.cleanup import excluir_chunks


UPLOAD_FOLDER_FILES = os.path.abspath('./upload')

@app.route('/')
def index():
    try:
        return jsonify({"message": "API em execução"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():

    try:

        # IDENTIFICA O TIPO DO ARTUIVO
        data = request.get_json()
        archive = data.get("archive")
        ex = archive.rsplit('.', 1)
        
        # CONVERTER VIDEO EM AUDIO
        if ex[1] in 'mp4':
            video_path = f"{UPLOAD_FOLDER_FILES}/video/{archive}"
            audio_output = f"{UPLOAD_FOLDER_FILES}/audio/{ex[0]}.wav"
            extrair_audio(video_path, audio_output)
            result = (f"Áudio extraído e salvo como: {audio_output}")

            return jsonify({"message": "Transcrição concluída", "result": result})
        
        if ex[1] in ['wav', 'mp3']:
            audio_path = f"{UPLOAD_FOLDER_FILES}/audio/{archive}"
            audio_chunks = dividir_audio(audio_path)
            output_text = f"{UPLOAD_FOLDER_FILES}/text/{ex[0]}.txt"
            transcribe_result = transcrever_audio(audio_chunks, output_text)
            excluir_chunks(audio_chunks)
            result = (f"Transcrição salva no arquivo: {output_text}")

            return jsonify({"message": "Transcrição concluída", "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# LISTAGEM DE ARQUIVOS
@app.route('/files', methods=['GET'])
def list_files():
    try:
        video_files = os.listdir(f"{UPLOAD_FOLDER_FILES}/video")
        audio_files = os.listdir(f"{UPLOAD_FOLDER_FILES}/audio")
        text_files = os.listdir(f"{UPLOAD_FOLDER_FILES}/text")
        return jsonify(
            {
                "videos": video_files,
                "audios": audio_files,
                "texts": text_files
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CRIAÇÃO DO ARQUIVO
@app.route('/file', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Arquivo não encontrado"}), 400
        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "Arquivo inválido"}), 400
        
        if file:
            ext = file.filename.rsplit('.', 1)[1].lower()
            timestamp = int(time.time())
            filename = file.filename.rsplit('.', 1)[0]
            new_filename = f"{filename}_{timestamp}.{ext}"

            if ext in ['mp3', 'wav']:
                file.save(f"{UPLOAD_FOLDER_FILES}/audio/{new_filename}")
                return jsonify(
                    {
                    "message": f"Arquivo {new_filename} salvo com sucesso",
                    "path": f"{UPLOAD_FOLDER_FILES}/audio/{new_filename}",
                    "filename": new_filename
                    }), 200
            elif ext in ['mp4', 'avi']:
                file.save(f"{UPLOAD_FOLDER_FILES}/video/{new_filename}")
                return jsonify({
                    "message": f"Arquivo {new_filename} salvo com sucesso",
                    "path": f"{UPLOAD_FOLDER_FILES}/video/{new_filename}",
                    "filename": new_filename
                    }), 200
            else:
                return jsonify({"error": "Tipo de arquivo inválido"}), 400
        return "sucesso"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#RENOMEAR ARQUIVO
@app.route('/file/<file_type>/<filename>', methods=['PUT'])
def rename_file(file_type, filename):
    data = request.get_json()
    ex = filename.rsplit('.', 1)
    new_filename = f"{data.get('name')}.{ex[1]}"
    if not new_filename:
        return jsonify({'error': 'Nome do arquivo não informado'}), 400

    if file_type == 'audio':
        folder = f"{UPLOAD_FOLDER_FILES}/audio"
    elif file_type == 'video':
        folder = f"{UPLOAD_FOLDER_FILES}/video"
    elif file_type == 'text':
        folder = f"{UPLOAD_FOLDER_FILES}/text"
    else:
        return jsonify({'error': 'Tipo de arquivo inválido'}), 400

    file_path = os.path.join(folder, filename)
    new_file_path = os.path.join(folder, new_filename)

    if os.path.exists(file_path):
        os.rename(file_path, new_file_path)
        return jsonify({'message': 'Arquivo renomeado com sucesso'}), 200
    else:
        return jsonify({'error': 'Arquivo não encontrado'}), 404

# DELETAR ARQUIVO
@app.route('/file/<file_type>/<filename>', methods=['DELETE'])
def delete_file(file_type, filename):
    if file_type == 'audio':
        folder = f"{UPLOAD_FOLDER_FILES}/audio"
    elif file_type == 'video':
        folder = f"{UPLOAD_FOLDER_FILES}/video"
    elif file_type == 'text':
        folder = f"{UPLOAD_FOLDER_FILES}/text"
    else:
        return jsonify({'error': 'Tipo de arquivo inválido'}), 400

    file_path = os.path.join(folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'Arquivo removido com sucesso!'}), 200
    else:
        return jsonify({'error': 'Arquivo não encontrado'}), 404

# LISTA ARQUIVOS