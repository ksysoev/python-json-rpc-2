"""JSON RPC Server

Package for work with rpc server
"""

from .router import Router
from .request import RequestFactory
from .response import ErrorResponse
from .exceptions import InvalidRequest, ParserError

class Server():
    """Class which represent JSON RPC server"""
    def __init__(self, router: Router = Router,
                 request_factory: RequestFactory = RequestFactory,
                 ):

        self.router = router
        self.request_factory = request_factory

    def dispatch(self, request_data: str):
        """Method for handling JSON RPC requests"""
        try:
            request = self.request_factory.make_request(request_data)
        except (InvalidRequest, ParserError) as error:
            return ErrorResponse(error)

        return request.proccess(self.router)
          