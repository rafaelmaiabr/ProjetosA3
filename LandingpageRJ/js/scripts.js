document.getElementById('send').addEventListener('click', function() {
  // Get input values
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
  const telefone = document.getElementById('telefone').value;

  // Display message
  alert(`${nome}, obrigado por entrar em contato com a agencia RJ. Cotação enviada com sucesso!`);
});

// Conteudo Modal
document.getElementById('modalAjax').addEventListener('show.bs.modal', function (event) {

  const button = event.relatedTarget;

  const modalTitle = document.getElementById('modalAjaxLabel');
  const dataContent = button.getAttribute('data-content');

  if (dataContent) {
    modalTitle.innerHTML = `Cotação para reserva - ${dataContent}`;
    document.getElementById('tour_type').value = dataContent;
  }

});

// Formulario Ajax
function send_form() {
  const name = document.getElementById('tour_name').value;
  const telefone = document.getElementById('tour_phone').value;
  const email = document.getElementById('tour_email').value;
  const qnt = document.getElementById('tour_qnt').value;
  const comment = document.getElementById('tour_message').value;
  const type = document.getElementById('tour_type').value;

  $.ajax({
    url: 'http://localhost:8080/formPedido/form.php',
    type: 'POST',
    data: {
      name: name,
      phone: telefone,
      email: email,
      qnt: qnt,
      comment: comment,
      type: type
    },
    success: function (response) {
      alert('Formulário enviado com sucesso!');
      $('#modalAjax').modal('hide');
    },
    error: function (xhr, status, error) {
      alert('Erro ao enviar o formulário: ' + xhr.responseText);
    }
  });
}