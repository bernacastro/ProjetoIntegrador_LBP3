function toggleContent(button) {
  const targetId = button.getAttribute('data-target'); // Obtém o ID do formulário associado
  const content = document.getElementById(targetId); // Seleciona a div específica

  content.classList.toggle('show'); // Alterna a classe "show" na div correspondente
  button.classList.toggle('active'); // Alterna a classe "active" no botão clicado
}

// Código para a Sidenav

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}
