document.getElementById('send').addEventListener('click', function() {
  // Get input values
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
  const telefone = document.getElementById('telefone').value;

  // Display message
  alert(`${nome}, obrigado por entrar em contato com a agencia RJ. Cotação enviada com sucesso!`);
});