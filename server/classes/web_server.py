from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import os
from email.utils import formatdate

from server.classes.specifications import Specifications


class WebServer:
    def __init__(self, documents, errors):
        self.web_server = socket(AF_INET, SOCK_STREAM)
        self.address = 'localhost'
        self.web_server.bind((self.address, 4000))
        self.web_server.listen()
        self.inspected_folder = documents
        self.errors_folder = errors

        try:
            os.mkdir(self.inspected_folder)
        except FileExistsError:
            pass

        self.documents_list = os.listdir(self.inspected_folder)

    def handle_error(self, sk_client, error_type):
        first_line = f'HTTP/1.1 {error_type} '
        if error_type == '400':
            first_line += 'Bad Request\r\n'
        elif error_type == '404':
            first_line += 'Not Found\r\n'
        elif error_type == '505':
            first_line += 'HTTP Version Not Supported\r\n'
        archive = f'{self.errors_folder}/html{error_type}.html'
        response = ''
        response += first_line
        response += f'Date: {formatdate(localtime=False, usegmt=True)}\r\n'
        response += f'Server: {self.address} (Windows)\r\n'
        response += f'Content-Length: {os.path.getsize(archive)}'
        response += 'Content-Type: text/html\r\n'
        response += '\r\n'
        arq = open(archive, 'r')
        content = arq.read()
        response += content
        sk_client.send(response.encode())

    def handle_success(self, specifications, sk_client):
        archive = self.inspected_folder + specifications.order
        if specifications.contenttype is not None:
            response = ''
            response += 'HTTP/1.1 200 OK\r\n'
            response += f'Date: {formatdate(localtime=False, usegmt=True)}\r\n'
            response += f'Server: {self.address} (Windows)\r\n'
            response += f'Content-Length: {os.path.getsize(archive)}\r\n'
            response += f'Content-Type: {specifications.contenttype}\r\n'
            response += '\r\n'
            sk_client.send(response.encode())
            print(response)
        try:
            arq = open(archive, 'rb')
            while True:
                parte = arq.read(1024)
                if len(parte) == 0:
                    break
                sk_client.send(parte)
        except PermissionError:
            path = archive
            if self.inspected_folder in path:
                path = path.split(self.inspected_folder + '/')[1]
                path += '/'
            if ' ' in path:
                path = path.split(' ')
                path = '%20'.join(path)
            self.create_index(sk_client, os.listdir(f'{archive}'), path)

    def create_index(self, sk_client, list, archive):
        response = ''
        response += 'HTTP/1.1 200 OK\r\n'
        response += f'Date: {formatdate(localtime=False, usegmt=True)}\r\n'
        response += f'Server: {self.address} (Windows)\r\n'
        response += 'Content-Type: text/html\r\n'
        response += '\r\n'
        sk_client.send(response.encode())
        crated_index = '<!DOCTYPE html>\r\n'
        crated_index += '<html>\r\n'
        crated_index += '<head>\r\n'
        crated_index += '<title> Index WebServer </title>\r\n'
        crated_index += '</head>\r\n'
        crated_index += '\r\n'
        crated_index += '<body>\r\n'
        crated_index += '<h1>documents disponiveis <h1>\r\n'
        if list:
            crated_index += '<ul>\r\n'
            for document in list:
                if document.split(".")[0] != 'favicon':
                    crated_index += f' <li><a href="http://localhost:4000/{archive}{document}"' \
                                    f'>{document.split(".")[0]}</a></li>\r\n'
            crated_index += '<ul>\r\n'
        crated_index += '</body>\r\n'
        crated_index += '</html>\r\n'
        print(response, crated_index)
        sk_client.send(crated_index.encode())

    def sanitize_message(self, msg_http):
        msg_http_sanitized = msg_http.split('\r\n')[0].split(' ')
        if msg_http_sanitized[1] == '/' and 'index.html' in self.documents_list:
            msg_http_sanitized[1] = 'index.html'
        cttp = msg_http_sanitized[1].split('.')[-1]
        if cttp[0] == '/':
            cttp = None
        if cttp == 'htm':
            cttp = 'html'
        elif cttp == 'jpg':
            cttp = 'jpeg'
        elif cttp == 'ico':
            cttp = 'ex-icon'
        elif cttp == 'txt':
            cttp = 'plain'
        if '%20' in msg_http_sanitized[1]:
            msg_http_sanitized[1] = msg_http_sanitized[1].split('%20')
            msg_http_sanitized[1] = ' '.join(msg_http_sanitized[1])
        return Specifications(msg_http_sanitized[0], msg_http_sanitized[1], cttp, msg_http_sanitized[2])

    def receive_message(self, sk_client):
        while True:
            msg_http = sk_client.recv(2048).decode()
            if msg_http:
                print(msg_http)
                try:
                    specifications = self.sanitize_message(msg_http)

                    if specifications.order == '/':
                        self.create_index(
                            sk_client, self.documents_list, '')

                    elif specifications.order[1:].split('/')[0] not in self.documents_list:
                        self.handle_error(sk_client, 404)
                        print('erro 404\n')

                    elif specifications.version.split('/')[1] != '1.1':
                        self.handle_error(sk_client, 505)
                        print('erro 505\n')

                    else:
                        self.handle_success(specifications, sk_client)
                        print('200 ok\n')
                except:
                    print('erro 400\n')
                    self.handle_error(sk_client, 400)

    def start_server(self):
        while True:
            (sock_client, address_client) = self.web_server.accept()

            Thread(target=self.receive_message,
                   args=(sock_client)).start()
