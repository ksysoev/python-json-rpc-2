import json

class Response():
    version = '2.0'
    def __init__(self, request, result):
        self.request = request
        self.result = result

        self.is_notification = False
        if not request.is_batch:
            self.is_notification = request.is_notification()

    def get_raw(self):
        assert not self.request.is_batch

        if self.is_notification:
            return None

        if isinstance(self.result, Response):
            return self.result.get_raw()

        return {'jsonrpc': self.version,
                'result': self.result,
                'id': self.request.id}

    def __str__(self):
        if self.request.id is None:
            return ''

        return json.dumps(self.get_raw())

class ErrorResponse(Response):
    def __init__(self, error, request=None):
        self.id = None
        self.is_notification = None
        self.error = error

        if request:
            self.id = request.id
            self.is_notification = request.is_notification()

    def get_raw(self):
        if self.is_notification:
            return None

        return {'jsonrpc': self.version,
                'error': self.error.get_data(),
                'id': self.id}


    def __str__(self):
        if self.is_notification:
            return ''

        return json.dumps(self.get_raw())



class BatchResponse():
    version = '2.0'
    def __init__(self, request, result):
        self.request = request
        self.result = result

        self.is_notification = False
        if not request.is_batch:
            self.is_notification = request.is_notification()

    def get_raw(self):
        responses = []
        for req, res in zip(self.request.requests, self.result):
            if isinstance(res, Response):
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