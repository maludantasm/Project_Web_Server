# Project_Web_Server

# Deverá ser desenvolvido um servidor WEB;
- Deverá implementar o protocolo HTTP/1.1, apenas o método
GET;

- O servidor terá que ser capaz de retornar diversos tipos de arquivos (por
ex: html, htm, css, js, png, jpg, svg...);

- Ou seja, deverá conseguir manipular tanto arquivos de texto,
quanto arquivos binários;

- O servidor deverá ser capaz de transmitir arquivos de tamanho muito
grande;

# Os requisitos mínimos (devem ser implementados obrigatoriamente) são
o desenvolvimento das respostas com os códigos de resposta a seguir:

  - 200 OK:
    Requisição bem-sucedida, objeto requisitado será enviado
  - 400 Bad Request:
    Mensagem de requisição não entendida pelo servidor,
    nesse caso o cliente escreveu a mensagem de requisição
    com algum erro de sintaxe;

  - 403 Forbidden:
    O cliente não tem direitos de acesso ao conteúdo, portanto
    o servidor está rejeitando dar a resposta.

  - 404 Not Found
    - Documento requisitado não localizado no servidor;
    v. 505 Version Not Supported
   - A versão do HTTP utilizada não é suportada neste
    servidor.

- Com exceção do código 200, o servidor deverá enviar obrigatoriamente
um arquivo html personalizado informando o respectivo erro;

- Se a pasta requisitada não contiver um arquivo index.html ou index.htm,
o servidor deverá criar uma página html para navegar pelas pastas,
semelhante ao que apache faz (que navega nas pastas de forma
semelhante ao windows explorer, nautilus e afins...);

- O uso de sockets TCP é obrigatório:
