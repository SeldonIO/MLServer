from fastapi import status
from fastapi.responses import Response

from ..handlers import DataPlane


class Endpoints:
    """
    Implementation of REST endpoints.
    These take care of the REST/HTTP-specific things and then delegate the
    business logic to the internal handlers.
    """

    def __init__(self, data_plane: DataPlane):
        self._data_plane = data_plane

    def live(self) -> Response:
        #  is_live = self._handlers.live()
        return Response(status_code=status.HTTP_200_OK)
