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
    """
    Custom request handler for an image hosting server.

    Handles HTTP GET/POST requests to manage image hosting functionality,
    including uploading and retrieving images.
    """

    server_version = 'Image Hosting Server v0.1'
    def __init__(self, request, client_address, server):
        """
        Initializes the request handler and configures route mappings.

        Args:
        request: The client's request object.
        client_address: The address of the client.
        server: The server instance handling the request.
        """
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
        """
        Handles the GET request for retrieving the list of images.

        Responds with a JSON structure containing the filenames
        of all images stored in the IMAGESTORE_PATH directory.
        """
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'images': next(os.walk(IMAGESTORE_PATH))[2]
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))


    def get_upload(self):
        """
        Handles the GET request for the upload page.

        Responds with the upload.html file to allow users to upload images.
        """
        self.send_html('upload.html', code =200)


    def post_upload(self):
        """
        Handles the POST request for uploading images.

        Validates the file size and extension, then saves the file with
        a unique identifier. Provides an appropriate response if the
        upload fails or succeeds.
        """
        file_size = int(self.headers.get('Content-Length'))
        if file_size > MAX_FILE_SIZE:
            logger.warning(f'file size err ')
            self.send_html('file_to_large.html', code=413)
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
        """
        Sends an HTML file as a response to the client.

        Args:
            file_path (str): The relative path to the HTML file.
            code (int): The HTTP status code (default: 200).
        """
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(STATIC_PATH + file_path, 'rb') as file:
            self.wfile.write(file.read())

        # handles all GET requests
    def do_GET(self):
        """
        Handles all HTTP GET requests.

        Routes the request path to the appropriate handler function,
        or returns a 404 response if the path is undefined.
        """
        logger.info(f'GET {self.path}')
        self.get_routes.get(self.path, self.default)()

    def do_POST(self):
        """
        Handles all HTTP POST requests.

        Routes the request path to the appropriate handler function,
        or returns a 404 response if the path is undefined.
        """

        logger.info(f'POST {self.path}')
        self.post_routes.get(self.path, self.default)()


# noinspection PyTypeChecker
def run(server_class=HTTPServer, handler_class=ImageHostingHTTPRequestHandler):
    """
    Starts the HTTP server for image hosting.

    This function initializes and runs the server, handling incoming
    connections until interrupted.

    Args:
        server_class: The class to use for the server (default: HTTPServer).
        handler_class: The request handler class (default: ImageHostingHTTPRequestHandler).
    """

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
