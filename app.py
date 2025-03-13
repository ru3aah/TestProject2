import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from uuid import uuid4

from loguru import logger

SERVER_ADDRESS = ('0.0.0.0', 8000)
STATIC_PATH = 'static/'
IMAGESTORE_PATH = 'images/'
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
MAX_FILE_SIZE = 1024 * 1024 * 5  # 5 MB
LOG_PATH = 'logs/'
LOG_FILE = 'app.log'


logger.add(LOG_PATH + LOG_FILE, format='[{time:YY-MM-DD HH:mm:ss}] {level}: '
                                       '{message}', level='INFO')


class ImageHostingHTTPRequestHandler(BaseHTTPRequestHandler):
    server_version = 'Image Hosting Server v0.1'
    def __init__(self, request, client_address, server):
        self.get_routes = {
            '/api/images': self.get_images,
            '/upload': self.get_upload
        }
        self.post_routes = {
            '/upload': self.post_upload,
        }
        self.default = lambda : self.send_html('404.html', code=404)
        super().__init__(request, client_address, server)


    def get_images(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'images': next(os.walk(IMAGESTORE_PATH))[2]
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))


    def get_upload(self):
        self.send_html('upload.html', code =200)


    def post_upload(self):
        file_size = int(self.headers.get('Content-Length'))
        if file_size > MAX_FILE_SIZE:
            logger.warning(f'file size err ')
            self.send_html('file_too_large.html', code=413)
            return
        data = self.rfile.read(file_size)
        _, file_ext = os.path.splitext(self.headers.get('Filename'))
        image_id = uuid4()
        if file_ext not in ALLOWED_EXTENSIONS:
            logger.warning(f'wrong file extension')
            self.send_html('invalid_file_type.html', code=400)
            return
        with open(IMAGESTORE_PATH + f'{image_id}{file_ext}', 'wb') as file:
            file.write(data)
        self.send_html('upload_success.html')


    def send_html(self, file_path, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(STATIC_PATH + file_path, 'rb') as file:
            self.wfile.write(file.read())

        # handles all GET requests
        def do_GET(self):
            logger.info(f'GET {self.path}')
            self.get_routes.get(self.path, self.default)()

        def do_POST(self):
            logger.info(f'POST {self.path}')
            self.post_routes.get(self.path, self.default)()


# noinspection PyTypeChecker
def run(server_class=HTTPServer, handler_class=ImageHostingHTTPRequestHandler):
    httpd = server_class(SERVER_ADDRESS, handler_class)
    logger.info(f'Server is running at {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt received, exiting.')
        httpd.server_close()
    finally:
        logger.info('Server has been shut down.')


if __name__ == '__main__':
        run()
