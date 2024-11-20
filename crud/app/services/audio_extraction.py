import moviepy.editor as mp

def extrair_audio(video_path, audio_output):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output)
    print(f"Áudio extraído e salvo como: {audio_output}")
