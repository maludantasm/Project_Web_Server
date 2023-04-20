from components.web_server import *
from config import *
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config_file_path = os.path.join(dir_path, 'serverConfig.txt')

documents, errors = config(open(config_file_path, 'r'))
server = WebServer(documents, errors)
server.start_server()
