from components.web_server import *
from config import *

documents, errors = config(open('serverConfig.txt', 'r'))
print(documents)
server = WebServer(documents, errors)
server.start_server()
