import json


class BaseResponse():
    version = '2.0'

class Response(BaseResponse):

    def __init__(self, request, result):
        self.request = request
        self.result = result

    def get_raw(self):
        if isinstance(self.result, BaseResponse):
            return self.result.get_raw()

        return {'jsonrpc': self.version,
                'result': self.result,
                'id': self.request.id}

    def __str__(self):
        if self.request.id is None:
            return ''

        return json.dumps(self.get_raw())

class EmptyResponse(BaseResponse):

    def get_raw(self):
        return None

    def __str__(self):
       return ''

class ErrorResponse(BaseResponse):
    def __init__(self, error, request=None):
        self.id = None
        self.error = error

        if request:
            self.id = request.id

    def get_raw(self):
        return {'jsonrpc': self.version,
                'error': self.error.get_data(),
                'id': self.id}


    def __str__(self):
        return json.dumps(self.get_raw())



class BatchResponse(BaseResponse):
    
    def __init__(self, request, result):
        self.request = request
        self.result = result

    def get_raw(self):
        responses = []
        for req, res in zip(self.request.requests, self.result):
            if isinstance(res, BaseResponse):
                raw_response = res.get_raw()
                if raw_response is None:
                    continue

                responses.append(raw_response)
                continue

            responses.append(Response(req, res).get_raw())

        return responses

    def __str__(self):
        raw_response = self.get_raw()
            
        if not raw_response:
            return ''

        return json.dumps(raw_response)