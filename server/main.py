from server.classes.web_server import WebServer
from server.utils.config import config

documents, errors = config(open('ConfiguracoesServidor.txt', 'r'))
server = WebServer(documents, errors)
server.start_server()
