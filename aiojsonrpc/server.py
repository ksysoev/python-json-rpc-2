from .router import Router
from .request import RequestFactory
from .response import Response, ErrorResponse
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

        results = []
        for single_request in request:
            if isinstance(single_request, Response):
                results.append(single_request)
                continue

            try:
                method = self.router.dispatch(single_request)
                args, kwargs = single_request.get_params()
                result = method(*args, **kwargs)
            except MethodNotFound as error:
                result = ErrorResponse(error, single_request)
            
            results.append(result)
        
        return Response(request,results)
          