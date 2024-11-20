import os

def excluir_chunks(chunks):
    for i in range(len(chunks)):
        os.remove(f"chunk{i}.wav")
