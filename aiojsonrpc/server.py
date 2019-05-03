from .router import Router
from .request import RequestFactory
from .response import Response, ErrorResponse, BatchResponse
from .exceptions import MethodNotFound, InvalidRequest, ParserError

class Server():
    def __init__(self, router:Router = Router, 
                 request_factory:RequestFactory = RequestFactory,
                 ):

        self.router = router
        self.request_factory = request_factory
        
    def dispatch(self, request_data:str):
        try:
            request = self.request_factory.make_request(request_data)
        except (InvalidRequest, ParserError) as error:
            return ErrorResponse(error)

        return request.proccess(self.router)
          