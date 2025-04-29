"""
Image Hosting Server Emulation for local host on 8000
2nd Project for Python full stack course at JetBrainAcademy
"""

from http.server import HTTPServer

from loguru import logger

from DB_Manager import DBManager
from Image_Hosting_Handler import ImageHostingHttpRequestHandler
from Router import Router
from settings import SERVER_ADDRESS


def run(server_class=HTTPServer,
        handler_class=ImageHostingHttpRequestHandler) -> None:
    """
    Initialize the image hosting server and start serving requests.

    This function sets up the necessary database tables, configures routing for
    handling HTTP GET, POST, and DELETE requests, and starts the HTTP server
    to listen for incoming connections.

    Parameters:
    server_class (type): The server class to instantiate.
    Defaults to HTTPServer.
    handler_class (type): The request handler class to use.
    Defaults to ImageHostingHttpRequestHandler.

    Routes:
    - GET /api/images/: Retrieves images.
    - GET /api/images_count/: Retrieves the count of images.
    - POST /upload/: Uploads a new image.
    - DELETE /api/delete/<image_id>: Deletes an image by ID.

    The server listens on the address specified in the SERVER_ADDRESS setting.
    It runs indefinitely until interrupted by a keyboard interrupt, at which
    point it shuts down gracefully.
    """
    DBManager().init_tables()
    router = Router()
    router.add_route('GET', '/api/images/',
                     handler_class.get_images)
    router.add_route('GET', '/api/images_count/',
                     handler_class.get_images_count)
    router.add_route('POST', '/upload/', handler_class.post_upload)
    router.add_route('DELETE', '/api/delete/<image_id>',
                     handler_class.delete_image)

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