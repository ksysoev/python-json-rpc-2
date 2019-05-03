import json
from .exceptions import InvalidRequest, ParserError, MethodNotFound
from .response import Response, ErrorResponse, BatchResponse



class RequestFactory():
    @classmethod
    def make_request(cls, raw_json: str):
        try:
            data = json.loads(raw_json)
        except (TypeError, json.decoder.JSONDecodeError):
            raise ParserError('Invalid request format')

        if isinstance(data, list):
            return BatchReuest(data)
        elif isinstance(data, dict):
            return Reuest(data)
        
        raise InvalidRequest('Invalid request format')
        

        


class ReuestBase():

    def proccess(self):
        pass

class Reuest(ReuestBase):

    is_batch = False

    def __init__(self, request_data, *args, **kwargs):
        
        if not isinstance(request_data, dict):
            raise InvalidRequest('Invalid request format')

        super().__init__(*args, **kwargs)
        self.id = request_data.get('id', None)
        
        self.params = request_data.get('params', {})

        if not isinstance(self.params,(dict, list)):
            raise InvalidRequest(' There is no method name')
        
        try:
            self.method = request_data['method']
        except KeyError:
            raise InvalidRequest(' There is no method name')

    def get_params(self):
        
        if isinstance(self.params, (list, tuple)):
            return self.params, {}

        return [], self.params

    def proccess(self, router):
        try:
            method = router.dispatch(self)
            args, kwargs = self.get_params()
            result = method(*args, **kwargs)
        except MethodNotFound as error:
            return ErrorResponse(error, self)

        return Response(self, result)

    def is_notification(self):
        return True if self.id is None else False


class BatchReuest(ReuestBase):
    is_batch = True

    def __init__(self, request_data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(request_data, list):
            raise InvalidRequest('Invalid request format')

        if len(request_data) == 0:
            raise InvalidRequest('Invalid request format')

        self.requests = []
        for request in request_data:
            try:
                request = Reuest(request)
            except (InvalidRequest, ParserError) as error:
                request = ErrorResponse(error)

            self.requests.append(request)

    def proccess(self, router):
        results = []
        for single_request in self.requests:
            if isinstance(single_request, Response):
                results.append(single_request)
                continue

            try:
                method = router.dispatch(single_request)
                args, kwargs = single_request.get_params()
                result = method(*args, **kwargs)
            except MethodNotFound as error:
                result = ErrorResponse(error, single_request)
            
            results.append(result)
        
        return BatchResponse(self, results)

        