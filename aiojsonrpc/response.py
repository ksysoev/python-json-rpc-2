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

        if isinstance(self.result[0], Response):
            return self.result[0].get_raw()

        return {'jsonrpc': self.version,
                'result': self.result[0],
                'id': self.request.id}

    def __str__(self):
        if self.request.is_batch:
            responses = []
            for req, res in zip(self.request, self.result):
                if isinstance(res, Response):
                    raw_response = res.get_raw()
                    if raw_response is None:
                        continue

                    responses.append(raw_response)
                    continue

                responses.append(Response(req, [res]).get_raw())

            if not responses:
                return ''

            return json.dumps(responses)

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
