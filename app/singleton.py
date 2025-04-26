"""
Provides a Singleton metaclass to implement the Singleton design pattern.
"""

class SingletonMeta(type):
    """
    Metaclass for implementing the Singleton design pattern. This ensures that
    a class using this metaclass can have only one instance and provides global
    access to that instance.

    This behavior is achieved by overriding the `__call__` method, which checks
    if an instance of the class already exists. If an instance exists,
    it returns the existing instance. Otherwise, it creates a new instance
    and stores it in an internal dictionary.

    :cvar _instances: Dictionary holding references to the single instances of
        each class using this metaclass.
    :type _instances: dict
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]