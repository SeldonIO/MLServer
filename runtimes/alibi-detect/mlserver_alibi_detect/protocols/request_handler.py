import numpy as np


class RequestHandler(object):
    def __init__(self, request: dict):
        self.request = request

    def validate(self):
        """
        Validate the request

        """
        raise NotImplementedError

    def extract_request(self) -> np.array:
        """
        Extract the request

        Returns
        -------
             A list
        """
        raise NotImplementedError
