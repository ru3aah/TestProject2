"""
Image Hosting Server Emulation for local host on 8000
2nd Project for Python full stack course at JetBrainAcademy
"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from uuid import uuid4

from loguru import logger

SERVER_ADDRESS = ('0.0.0.0', 8000)
STATIC_PATH = 'static/'
IMAGES_PATH = 'images/'
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
MAX_FILE_SIZE = 5 * 1024 * 1024
LOG_PATH = 'logs/'
LOG_FILE = 'app.log'

logger.add(LOG_PATH + LOG_FILE,
           format='[{time:YY-MM-DD HH:mm:ss}] {level}: {message}',
           level='INFO')


class ImageHostingHttpRequestHandler(BaseHTTPRequestHandler):
    """
    A custom HTTP request handler for an image hosting server.

    This handler serves routes for uploading images and retrieving the list
    of uploaded images. It supports GET and POST methods, handles large file uploads,
    and enforces file type restrictions.
    """
    server_version = 'Image Hosting Server v0.1'

    def __init__(self, request, client_address, server):
        """
        Initialize the HTTP request handler with required configurations.

        Parameters:
            request (bytes): The raw HTTP request.
            client_address (tuple): The client address.
            server (HTTPServer): The HTTP server instance.

        Routes:
            - GET '/api/images': Returns a list of uploaded images.
            - POST '/upload/': Handles image upload.
        """

        self.get_routes = {'/api/images': self.get_images}
        self.post_routes = {'/upload/': self.post_upload}
        self.default_response = lambda: self.send_html('404.html', 404)
        super().__init__(request, client_address, server)


    def get_images(self):
        """
        Handle GET requests for retrieving the list of uploaded images.

        Sends a JSON response containing the filenames of images located in
        the 'images/' directory.
        """

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'images': next(os.walk(IMAGES_PATH))[2]}
        self.wfile.write(json.dumps(response).encode('utf-8'))


    def post_upload(self):
        """
        Handle POST requests for uploading images.

        Validates the file size and type before saving it to the server.
        Logs warnings for invalid files. Responds with success or failure pages.

        - If valid: The image is saved using a UUID and the client is redirected.
        - If invalid: Returns appropriate HTTP error statuses (413 for size limit,
          400 for invalid file types).
        """

        length = int(self.headers.get('Content-Length'))
        if length > MAX_FILE_SIZE:
            logger.warning('File too large')
            self.send_html('upload_failed.html', 413)
            return
        data = self.rfile.read(length)
        _, ext = os.path.splitext(self.headers.get('Filename'))
        image_id = uuid4()
        if ext not in ALLOWED_EXTENSIONS:
            logger.warning('File type not allowed')
            self.send_html('upload_failed.html', 400)
            return
        with open(IMAGES_PATH + f'{image_id}{ext}', 'wb') as file:
            file.write(data)
        self.send_html('upload_success.html',
                       headers={'Location': f'http://localhost/'
                                            f'{IMAGES_PATH}/{image_id}{ext}'})


    def send_html(self, file_path, code=200, headers=None):
        """
        Sends an HTML response using a static file.

        Parameters:
            file_path (str): Path to the HTML file to be sent.
            code (int): HTTP status code for the response. Defaults to 200.
            headers (dict): Additional HTTP headers to include in the response.
        """

        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()
        with open(STATIC_PATH + file_path, 'rb') as file:
            self.wfile.write(file.read())


    def do_GET(self):
        """
        Handle incoming GET requests by routing them to the appropriate handler.

        Logs the request and executes the route handler based on the requested path.
        If the route is not found, serves a 404 page.
        """

        logger.info(f'GET {self.path}')
        self.get_routes.get(self.path, self.default_response)()


    def do_POST(self):
        """
        Handle incoming POST requests by routing them to the appropriate handler.

        Logs the request and executes the route handler based on the requested path.
        If the route is not found, serves a 404 page.
        """
        logger.info(f'POST {self.path}')
        self.post_routes.get(self.path, self.default_response)()


def run(server_class=HTTPServer, handler_class=ImageHostingHttpRequestHandler):
    """
    Start the HTTP server with the specified handler class.

    Parameters:
        server_class (type): HTTP server class to be instantiated.
        handler_class (type): Request handler class to handle incoming requests.

    The server listens on the address defined in SERVER_ADDRESS and handles
    incoming requests until interrupted.
    """
    httpd = server_class(SERVER_ADDRESS, handler_class)
    logger.info(f'Serving on http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt received, exiting.')
        httpd.server_close()
    finally:
        logger.info('Server stopped.')


if __name__ == '__main__':
    run()