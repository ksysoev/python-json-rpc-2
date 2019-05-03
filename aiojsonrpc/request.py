import json
from .exceptions import InvalidRequest, ParserError
from .response import ErrorResponse



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

    def proccess(self):
        pass

    def is_processed(self):
        pass

    def is_notification(self):
        return True if self.id is None else False

    def __iter__(self):
        return iter([self])


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

    def proccess(self, callback):
        results = []
        for request in self.requests:
            results.append(request.proccess(callback))

        return results

    def __iter__(self):
        return iter(self.requests)
        

        