"""
This module provides a Router class for managing HTTP routes.

Key Classes:
- Router: Handles routing by associating URL paths with handler functions.

Dependencies:
- re: Used for compiling and matching regular expressions.
- loguru: Used for logging purposes.
"""

import re

from loguru import logger

from singleton import SingletonMeta


class Router(metaclass=SingletonMeta):
    """
    Handles routing for HTTP methods and paths.

    This class manages a set of routes and provides functionality for adding
    routes and resolving paths to their corresponding handlers.
    It supports HTTP methods such as GET, POST, DELETE, and it uses regular
    expressions for path matching.

    :ivar routes: A dictionary holding routes for each HTTP method.
    The keys
                  are HTTP methods ('GET', 'POST', 'DELETE'), and the values
                  are dictionaries where keys are compiled regex patterns
                  representing paths,
                  and values are their associated handlers.
    :type routes: dict
    """
    def __init__(self):
        self.routes = {
            'GET': {},
            'POST': {},
            'DELETE': {},
        }

    @staticmethod
    def convert_path(path) -> str:
        """
        Converts a URL path containing placeholders to a
        regex-compatible pattern.

        This method replaces placeholders
        in the format ``<placeholder_name>`` with a
        named group ``(?P<placeholder_name>[^/]+)`` suitable for use in regular
        expressions.
        This allows dynamic parsing of paths to extract named groups
        based on placeholder names.

        :param path: A string
                        representing the URL containing placeholders
                        in the format ``<placeholder_name>``.
        :type path: str
        :return: A regex-compatible string
                where placeholders are replaced by corresponding named groups.
        :rtype: str
        """
        return re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)

    def add_route(self, method, path, handler) -> None:
        """
        Adds a new route to the routing table
        by compiling the given path pattern.

        This method registers a handler function
        associated with a specific HTTP
        method and path.
        The path is converted into a regular expression pattern,
        and the resulting compiled pattern is added to the routing table under
        the specified HTTP method.

        :param method: The HTTP method (e.g., 'GET', 'POST')
                to associate with the route.
        :type method: str
        :param path: The URL path pattern which can include
                dynamic segments to match.
        :type path: str
        :param handler: The function or callable to be executed
                        when the route matches.
        :type handler: Callable
        :return: None
        """
        pattern = self.convert_path(path)
        compiled = re.compile(pattern)
        self.routes[method][compiled] = handler

    def resolve(self, method, path) -> tuple[callable, dict]:
        """
        Resolves a method and path to a corresponding handler function
        and any extracted parameters from the request path.
        This process matches the path against the available routes
        for the specified HTTP method and returns the appropriate
        handler and extracted parameters, if found.
        If no match is found, it returns `None` and an empty dictionary.

        :param method: The HTTP method (e.g., 'GET', 'POST').
        :type method: str
        :param path: The request path to resolve into a handler.
        :type path: str
        :return: A tuple containing the resolved handler (callable)
        and a dictionary with extracted parameters from the path.
        If no match is found, returns (None, {}).
        """
        logger.info(f'Resolving {method} {path}')
        if method not in self.routes:
            return None, {}

        for pattern, handler in self.routes[method].items():
            match = pattern.match(path)
            if match:
                logger.info(f'Found handler for {method} {path}')
                kwargs = match.groupdict()
                return handler, kwargs
        return None, {}