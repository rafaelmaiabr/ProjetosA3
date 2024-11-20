const allowedFormats = {
  video: ['mp4', 'avi'],
  audio: ['wav', 'mp3'],
  text: ['txt']
};

document.getElementById('upload').addEventListener('click', function () {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];

  if (!file) {
    alert('Por favor, selecione um arquivo.');
    return;
  }

  const fileExtension = file.name.split('.').pop().toLowerCase();
  let fileType = '';

  if (allowedFormats.video.includes(fileExtension)) {
    fileType = 'video';
  } else if (allowedFormats.audio.includes(fileExtension)) {
    fileType = 'audio';
  } else if (allowedFormats.text.includes(fileExtension)) {
    fileType = 'text';
  } else {
    alert('Formato de arquivo não permitido.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  fetch('http://localhost:5000/file', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      alert('Arquivo enviado com sucesso.');
      fetchDocuments(); // Atualiza a lista de documentos após o upload
    })
    .catch(error => {
      console.error('Erro:', error);
      alert('Erro ao enviar o arquivo.');
    });
});

// LISTA ARQUIVOS
async function fetchDocuments() {
    try {
      const response = await fetch('http://localhost:5000/files');
      console.log('Response status:', response.status); // Log do status da resposta

      if (!response.ok) {
        throw new Error('Erro ao obter a lista de documentos.');
      }

      const data = await response.json();
      console.log('Data received:', data); // Log dos dados recebidos

      const documentList = document.getElementById('documentList');
      documentList.innerHTML = ''; // Limpa a lista atual

      const groupedFiles = {};

      // Função para extrair o nome do arquivo sem a extensão
      const getBaseName = (filename) => filename.split('.').slice(0, -1).join('.');

      // Função para adicionar um arquivo ao agrupamento
      const addToGroupedFiles = (type, filename) => {
        const baseName = getBaseName(filename);
        if (!groupedFiles[baseName]) groupedFiles[baseName] = { video: 'não possui', audio: 'não possui', text: 'não possui' };
        groupedFiles[baseName][type] = filename;
      };

      // Processa os vídeos, áudios e textos
      data.videos.forEach(video => addToGroupedFiles('video', video));
      data.audios.forEach(audio => addToGroupedFiles('audio', audio));
      data.texts.forEach(text => addToGroupedFiles('text', text));

      // Monta as linhas da tabela
      const rows = Object.keys(groupedFiles).map(baseName => {
        const { video, audio, text } = groupedFiles[baseName];

          return `
    <tr>
      <td>
        ${video !== 'não possui' ? `
        <button class="btn btn-sm btn-info renameVideo" onclick="renameFile('${video}')">
          <i class="fas fa-edit"></i></button>
        <button class="btn btn-sm btn-warning converter" onclick="converter('${video}')">
          <i class="fa fa-video"></i> <i class="fa fa-arrow-right"></i> <i class="fa fa-music"></i></button>
        <button class="btn btn-sm btn-danger removeVideo" onclick="deleteFile('${video}')">
          <i class="fa fa-xmark"></i></button>
        <button class="btn btn-sm btn-outline-primary" data-type="video" data-bs-toggle="modal" data-bs-target="#modalAjax">${video}</button>
        ` : video}
      </td>
      <td>
        ${audio !== 'não possui' ? `
        <button class="btn btn-sm btn-info" onclick="renameFile('${audio}')"><i class="fas fa-edit"></i></button>
        <button class="btn btn-sm btn-warning" onclick="converter('${audio}')"><i class="fa fa-music"></i> <i class="fa fa-arrow-right"></i> abc</button>
        <button class="btn btn-sm btn-danger removeAudio" onclick="deleteFile('${audio}')"><i class="fa fa-xmark"></i></button>
        <button class="btn btn-sm btn-outline-primary" data-type="audio" data-bs-toggle="modal" data-bs-target="#modalAjax">${audio}</button>
        ` : audio}
      </td>
      <td>
        ${text !== 'não possui' ? `
        <button class="btn btn-sm btn-info" onclick="renameFile('${text}')"><i class="fas fa-edit"></i></button>
        <button class="btn btn-sm btn-danger removeText" onclick="deleteFile('${text}')"><i class="fa fa-xmark"></i></button>
        <button class="btn btn-sm btn-outline-primary" data-type="text" data-bs-toggle="modal" data-bs-target="#modalAjax">${text}</button>
        ` : text}
      </td>
    </tr>
  `;
        }).join('');

        documentList.innerHTML = rows;
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao obter a lista de documentos.');
    }
  }

// RENOMEAR ARQUIVO
function renameFile(fileName) {
    // Solicita o novo nome ao usuário
    const newFileName = prompt(`Digite o novo nome para o arquivo ${fileName}:`);
    if (!newFileName || newFileName.trim() === '') {
      alert('O novo nome não pode estar vazio.');
      return;
    }

    // Determina o tipo de arquivo com base na extensão
    const fileType = fileName.endsWith('.mp4') ? 'video' :
      fileName.endsWith('.wav') ? 'audio' :
        fileName.endsWith('.txt') ? 'text' : null;

    if (!fileType) {
      alert('Tipo de arquivo inválido.');
      return;
    }

    const url = `http://localhost:5000/file/${fileType}/${fileName}`;

    // Envia a solicitação PUT para renomear o arquivo
    fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: newFileName.trim() }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro ao renomear o arquivo.');
        }
        return response.json();
      })
      .then(data => {
        alert(`Arquivo renomeado com sucesso para: ${data.newName || newFileName}`);
        // Atualiza a lista de documentos
        fetchDocuments();
      })
      .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao renomear o arquivo.');
      });
  }

// EXCLUIR ARQUIVO
function deleteFile(fileName) {
    if (!confirm(`Tem certeza de que deseja excluir o arquivo ${fileName}?`)) {
      return;
    }

    // Determina o tipo de arquivo com base na extensão
    const fileType = fileName.endsWith('.mp4') ? 'video' :
      fileName.endsWith('.wav') ? 'audio' :
        fileName.endsWith('.txt') ? 'text' : null;

    if (!fileType) {
      alert('Tipo de arquivo inválido.');
      return;
    }

    const url = `http://localhost:5000/file/${fileType}/${fileName}`;

    // Envia a solicitação DELETE para excluir o arquivo
    fetch(url, {
      method: 'DELETE',
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro ao excluir o arquivo.');
        }
        return response.json();
      })
      .then(data => {
        alert('Arquivo excluído com sucesso.');
        // Atualiza a lista de documentos
        fetchDocuments();
      })
      .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao excluir o arquivo.');
      });
  }

// CONVERTER ARQUIVO
function converter(fileName) {
  // Solicita confirmação do usuário
  const confirmacao = confirm(`Deseja converter o arquivo ${fileName}?`);
  if (!confirmacao) {
    return; // Cancela a operação se o usuário não confirmar
  }

  // URL e corpo da requisição
  const url = 'http://localhost:5000/transcribe';
  const requestBody = { archive: fileName };

  // Faz a solicitação POST para converter o arquivo
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  })
  .then(response => {
      console.log(response)
      if (!response.ok) {
        throw new Error('Erro ao converter o arquivo.');
      }
      return response.json();
    })
    .then(data => {
      alert(`Arquivo convertido com sucesso! Resultado: ${data.result || 'Sem detalhes'}`);
      // Opcional: atualize a lista de arquivos se necessário
      fetchDocuments();
    })
    .catch(error => {

      console.error('Erro:', error);
      alert('Erro ao converter o arquivo.');
    });
}

// VERIFICAR STATUS DO SERVIDOR
function checkServerStatus() {
  fetch('http://localhost:5000/')
    .then(response => {
      if (response.status === 200) {
        document.getElementById('serverStatus').textContent = 'online';
        document.getElementById('serverStatus').classList.remove('text-danger');
        document.getElementById('serverStatus').classList.add('text-success');
      } else {
        document.getElementById('serverStatus').textContent = 'offline';
        document.getElementById('serverStatus').classList.remove('text-success');
        document.getElementById('serverStatus').classList.add('text-danger');
      }
    })
    .catch(error => {
      document.getElementById('serverStatus').textContent = 'offline';
      document.getElementById('serverStatus').classList.remove('text-success');
      document.getElementById('serverStatus').classList.add('text-danger');
    });
}

// Modal Ajax
document.getElementById('modalAjax').addEventListener('show.bs.modal', function (event) {
  const button = event.relatedTarget;
  const fileType = button.getAttribute('data-type');
  const fileName = button.textContent;

  const modalTitle = document.getElementById('modalAjaxLabel');
  modalTitle.textContent = `Conteúdo do arquivo ${fileName}`;

  const modalBody = document.querySelector('#modalAjax .modal-body');
  modalBody.innerHTML = 'Carregando...';

  if (fileType === 'video') {
    modalBody.innerHTML = `
      <video controls autoplay style="width: 100%;">
          Seu navegador não suporta o elemento de vídeo.
        <source src="http://127.0.0.1:5500/crud/upload/video/${fileName}" type="video/mp4">
        Seu navegador não suporta o elemento de vídeo.
      </video>
    `;
  } else if (fileType === 'audio') {
    modalBody.innerHTML = `
      <audio controls autoplay>
        <source src="http://127.0.0.1:5500/crud/upload/audio/${fileName}" type="audio/mpeg">
        Seu navegador não suporta o elemento de áudio.
      </audio>
    `;
  } else if (fileType === 'text') {
    fetch(`http://127.0.0.1:5500/crud/upload/text/${fileName}`)
      .then(response => response.text())
      .then(data => {
        modalBody.textContent = data;
      })
      .catch(error => {
        console.error('Erro:', error);
        modalBody.textContent = 'Erro ao carregar o conteúdo do arquivo.';
      });
  }
});

// Limpar conteúdo ao fechar o modal
document.getElementById('modalAjax').addEventListener('hide.bs.modal', function () {
  const modalBody = document.querySelector('#modalAjax .modal-body');
  modalBody.innerHTML = ''; // Remove o conteúdo
});

// Verifica o status do servidor ao carregar a página
window.onload = function () {
  checkServerStatus();
  fetchDocuments(); // Obtém a lista de documentos ao carregar a página
};
