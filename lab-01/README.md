# Lab 01 - Servidor Web

## Descrição

Este projeto tem como objetivo implementar um imples servidor web que recebe requisições HTTP do tipo GET utilizando sockets TCP. O servidor identifica o arquivo solicitado, busca no diretório local e retorna seu conteúdo ao cliente. Caso o arquivo não seja encontrado, deve ser retornada uma resposta HTTP com código `404 Not Found`. Além disso, o servidor utiliza threads para permitir o atendimento concorrente de múltiplas conexões.

## Uso

No diretório `lab-01`, execute o arquivo `server.py`:

    python server.py

Para testar o cliente na mesma máquina no servidor, basta fazer a seguinte requisição em algum navegador:

    http://localhost:12000/index.html

Caso esteja em outra máquina:

    http://<IP_SERVIDOR>:12000/index.html

Ou, também pode-se usar o `curl` pelo terminal:

    curl http://<IP_SERVIDOR>:12000/index.html

Nos casos acima, será retornada uma página html com a mensagem:

> "Welcome to my Web Server!"

Para testar o caso em que o arquivo não é encontrado, basta substituir "index.html" por qualquer outro nome de arquivo. A requisição irá retornar uma página com a mensagem:

> "404 Not Found"
