"""Request

Package contains classes which represents different classes for requests
"""

import json
from abc import ABCMeta
from funcsigs import signature
from .exceptions import (InvalidRequest, ParserError, MethodNotFound,
                         InvalidParams, InternalError, BaseRPCError)
from .response import Response, BaseResponse, ErrorResponse, BatchResponse, EmptyResponse


class RequestFactory():
    """Factory for producing requests objects"""

    @classmethod
    def make_request(cls, raw_json: str):
        """Method for creating Request object from json string"""

        try:
            data = json.loads(raw_json)
        except (TypeError, json.decoder.JSONDecodeError):
            raise ParserError('Invalid request format')

        if isinstance(data, list):
            return BatchReuest(data)

        return cls.make_single_request(data)

    @classmethod
    def make_single_request(cls, data: dict):
        """Method for creating single request object"""

        if not isinstance(data, dict):
            raise InvalidRequest('Invalid request format')

        request_id = data.get('id', None)

        if request_id is None:
            return NotificationRequest(data)

        return Reuest(data)


class ReuestBase(metaclass=ABCMeta):
    def proccess(self, router):
        pass

class Reuest(ReuestBase):

    def __init__(self, request_data, *args, **kwargs):

        if not isinstance(request_data, dict):
            raise InvalidRequest('Invalid request format')

        super().__init__(*args, **kwargs)
        self.id = request_data.get('id', None)

        self.params = request_data.get('params', {})

        if not isinstance(self.params, (dict, list)):
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
        except MethodNotFound as error:
            return ErrorResponse(error, self)

        args, kwargs = self.get_params()
        try:
            signature(method).bind(*args, **kwargs)
        except TypeError as error:
            return ErrorResponse(InvalidParams(error), self)

        try:
            result = method(*args, **kwargs)
        except BaseRPCError as error:
            return ErrorResponse(error, self)
        except Exception as error:
            return ErrorResponse(InternalError(error), self)

        return Response(self, result)


class NotificationRequest(Reuest):
    def proccess(self, router):
        super().proccess(router)

        return EmptyResponse()


class BatchReuest(ReuestBase):

    def __init__(self, requests_data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not isinstance(requests_data, list):
            raise InvalidRequest('Invalid request format')

        if not requests_data:
            raise InvalidRequest('Invalid request format')

        self.requests = []
        for request_data in requests_data:
            try:
                request = RequestFactory.make_single_request(request_data)
            except (InvalidRequest, ParserError) as error:
                request = ErrorResponse(error)

            self.requests.append(request)

    def proccess(self, router):
        responses = []
        for request in self.requests:
            if isinstance(request, BaseResponse):
                responses.append(request)
                continue

            response = request.proccess(router)

            responses.append(response)

        return BatchResponse(self, responses)
