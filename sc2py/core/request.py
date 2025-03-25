from enum import Enum
from typing import Dict, Any, Optional, List, Union
from sc2py.services.base import SCV2Service, SCV2BaseEndpoint

class SCV2RequestType(Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'

class SCV2QueryParameterType(Enum):
    FILTER = '$filter'
    SELECT = '$select'
    ORDERBY = '$orderby'
    SEARCH = '$search'
    TOP = '$top'
    SKIP = '$skip'
    EXCLUDE = '$exclude'
    COUNT = '$count'

class SCV2Request:
    """
    Represents a request to the SAP Sales/Service Cloud V2 API.
    This class holds all the necessary information to make a request.
    """
    def __init__(self, 
                 request_type: SCV2RequestType,
                 service: SCV2Service,
                 endpoint: SCV2BaseEndpoint,
                 resource_id: Optional[str] = None,
                 params: Optional[Dict[str, Any]] = None,
                 payload: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None):
        self.request_type = request_type
        self.service = service
        self.endpoint = endpoint
        self.resource_id = resource_id
        self.params = params or {}
        self.payload = payload
        self.headers = headers or {}

class SCV2RequestBuilder:
    """
    Builder for creating SCV2Request objects with a fluent interface.
    """
    def __init__(self):
        self.__request_type = None
        self.__service = None
        self.__endpoint = None
        self.__resource_id = None
        self.__params = {}
        self.__payload = None
        self.__headers = {}

    def get(self, service: SCV2Service, endpoint: SCV2BaseEndpoint) -> "SCV2RequestBuilder":
        self.__request_type = SCV2RequestType.GET
        self.__service = service
        self.__endpoint = endpoint
        return self

    def post(self, service: SCV2Service, endpoint: SCV2BaseEndpoint) -> "SCV2RequestBuilder":
        self.__request_type = SCV2RequestType.POST
        self.__service = service
        self.__endpoint = endpoint
        return self

    def patch(self, service: SCV2Service, endpoint: SCV2BaseEndpoint) -> "SCV2RequestBuilder":
        self.__request_type = SCV2RequestType.PATCH
        self.__service = service
        self.__endpoint = endpoint
        return self

    def put(self, service: SCV2Service, endpoint: SCV2BaseEndpoint) -> "SCV2RequestBuilder":
        self.__request_type = SCV2RequestType.PUT
        self.__service = service
        self.__endpoint = endpoint
        return self

    def delete(self, service: SCV2Service, endpoint: SCV2BaseEndpoint) -> "SCV2RequestBuilder":
        self.__request_type = SCV2RequestType.DELETE
        self.__service = service
        self.__endpoint = endpoint
        return self

    def with_resource_id(self, resource_id: str) -> "SCV2RequestBuilder":
        self.__resource_id = resource_id
        return self

    # Generic parameter method (still available for custom parameters)
    def with_param(self, param: Union[str, SCV2QueryParameterType], value: Any) -> "SCV2RequestBuilder":
        if isinstance(param, SCV2QueryParameterType):
            self.__params[param.value] = value
        else:
            self.__params[param] = value
        return self

    # Dedicated methods for common OData parameters
    def filter(self, expression: str) -> "SCV2RequestBuilder":
        self.__params[SCV2QueryParameterType.FILTER.value] = expression
        return self

    def select(self, fields: Union[str, List[str]]) -> "SCV2RequestBuilder":
        if isinstance(fields, list):
            self.__params[SCV2QueryParameterType.SELECT.value] = ",".join(fields)
        else:
            self.__params[SCV2QueryParameterType.SELECT.value] = fields
        return self

    def orderby(self, expression: str) -> "SCV2RequestBuilder":
        self.__params[SCV2QueryParameterType.ORDERBY.value] = expression
        return self

    def search(self, query: str) -> "SCV2RequestBuilder":
        self.__params[SCV2QueryParameterType.SEARCH.value] = query
        return self

    def top(self, count: int) -> "SCV2RequestBuilder":
        self.__params[SCV2QueryParameterType.TOP.value] = str(count)
        return self

    def skip(self, count: int) -> "SCV2RequestBuilder":
        self.__params[SCV2QueryParameterType.SKIP.value] = str(count)
        return self

    def exclude(self, fields: Union[str, List[str]]) -> "SCV2RequestBuilder":
        if isinstance(fields, list):
            self.__params[SCV2QueryParameterType.EXCLUDE.value] = ",".join(fields)
        else:
            self.__params[SCV2QueryParameterType.EXCLUDE.value] = fields
        return self

    def expand(self, relations: Union[str, List[str]]) -> "SCV2RequestBuilder":
        if isinstance(relations, list):
            self.__params[SCV2QueryParameterType.EXPAND.value] = ",".join(relations)
        else:
            self.__params[SCV2QueryParameterType.EXPAND.value] = relations
        return self

    def with_payload(self, payload: Dict[str, Any]) -> "SCV2RequestBuilder":
        self.__payload = payload
        return self

    def with_header(self, key: str, value: str) -> "SCV2RequestBuilder":
        self.__headers[key] = value
        return self

    def with_etag(self, etag: str) -> "SCV2RequestBuilder":
        self.__headers['If-Match'] = etag
        return self

    def build(self) -> SCV2Request:
        # Validate the configuration
        if not self.__request_type:
            raise ValueError("Request type is required")
        if not self.__service:
            raise ValueError("Service is required")
        if not self.__endpoint:
            raise ValueError("Endpoint is required")

        # Additional validation based on request type
        if self.__request_type in [SCV2RequestType.PATCH, SCV2RequestType.DELETE]:
            if not self.__resource_id:
                raise ValueError(f"Resource ID is required for {self.__request_type.value} requests")
        
        if self.__request_type in [SCV2RequestType.POST, SCV2RequestType.PATCH, SCV2RequestType.PUT]:
            if not self.__payload:
                raise ValueError(f"Payload is required for {self.__request_type.value} requests")
                
        if self.__request_type == SCV2RequestType.PATCH and 'If-Match' not in self.__headers:
            raise ValueError("ETag (If-Match header) is required for PATCH requests")

        return SCV2Request(
            request_type=self.__request_type,
            service=self.__service,
            endpoint=self.__endpoint,
            resource_id=self.__resource_id,
            params=self.__params,
            payload=self.__payload,
            headers=self.__headers
        )