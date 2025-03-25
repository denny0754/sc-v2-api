import requests

from functools import lru_cache

from scv2_api.services import SCV2BaseEndpoint, SCV2Service, InternalAPIEndpointSanitizer

from scv2_api.exceptions import SCV2InvalidEndpointException, SCV2ConnectionError, SCV2RequestError, SCV2TimeoutError

from scv2_api.core.request import SCV2Request, SCV2QueryParameterType, SCV2RequestType

class SCV2Session:

    # This must be set to the full domain name of the tenant.
    # Example: my1122334.de1.test.crm.cloud.sap
    __sc_host : str

    # Protocol to be used to call the SAP Sales/Service Cloud V2 API
    # Hardcoded to HTTPS, as HTTP is not supported nor secure.
    # No need to make the user chose between the two protocols.
    __sc_prot : str = 'https'

    # Whether or not to use SSL Verification. 
    # Default: `True`
    __sc_vssl : bool = True

    # The time in seconds after a hanging call can timeout.
    __sc_timeout : int = 60

    # The API base endpoint path
    __sc_api_base_path : str = '/sap/c4c/api/v1/'

    # This is the User that will perform the calls
    __sc_user : str
    # Password of the user.
    __sc_pass : str

    # Static request headers
    __sc_request_headers : dict

    # Persistent session
    __sc_session : requests.Session

    def __init__(self, sc_host : str, sc_user : str, sc_password : str, sc_verify_ssl : bool = True, sc_timeout : int = 60) -> None:

        if not sc_host:
            raise ValueError("Host cannot be empty")

        if not sc_user or not sc_password:
            raise ValueError("User credentials cannot be empty")

        if sc_timeout <= 0:
            raise ValueError("Timeout must be a positive integer")
        
        self.__sc_host = sc_host
        self.__sc_vssl = sc_verify_ssl
        self.__sc_timeout = sc_timeout
        self.__sc_user = sc_user
        self.__sc_pass = sc_password

        self.__sc_session = requests.Session()
        self.__sc_session.auth = (self.__sc_user, self.__sc_pass)
        self.__sc_session.verify = self.__sc_vssl

        self.__sc_request_headers = { }

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @lru_cache(maxsize=None)
    def __get_call_url(self, service : SCV2Service, endpoint : SCV2BaseEndpoint) -> str:
        return f"{self.__sc_prot}://{self.__sc_host}{self.__sc_api_base_path}{service.value}/{endpoint.value}"

    @lru_cache(maxsize=None)
    def __validate_service_endpoint(self, service : SCV2Service, endpoint : SCV2BaseEndpoint) -> None:
        # Veryfing that the passed endpoint is actually defined on the passed service.
        # If not, raise an exception.
        if(not InternalAPIEndpointSanitizer.is_valid_endpoint(service=service, endpoint=endpoint)):
            raise SCV2InvalidEndpointException(f'Endpoint {endpoint.name} is not defined on service {service.name}.')
        
    def __make_request(self, http_method : str, req_url : str, req_params : dict, req_payload : dict, req_headers : dict) -> requests.Response:

        response : requests.Response

        try:
            response = self.__sc_session.request(
                method=http_method.upper(),
                url=req_url,
                json=req_payload,
                params=req_params,
                headers=req_headers,
                timeout=self.__sc_timeout
                )
            return response
        except requests.ConnectionError as e:
            raise SCV2ConnectionError(f"Connection error: {str(e)}") from e
        except requests.Timeout as e:
            raise SCV2TimeoutError(f"Request timed out: {str(e)}") from e
        except requests.RequestException as e:
            raise SCV2RequestError(f"Request error: {str(e)}") from e

    def set_default_headers(self, headers : dict) -> None:
        self.__sc_request_headers = headers

    def get(self,
            service : SCV2Service,
            endpoint : SCV2BaseEndpoint,
            resource_id : str = None,
            filter : str = None,
            select : str = None,
            orderby : str = None,
            search : str = None,
            top : int = None,
            skip : int = None,
            exclude : str = None) -> requests.Response:

        # Validating both Service and Endpoint
        self.__validate_service_endpoint(service=service, endpoint=endpoint)

        # Generating the request URL
        req_url : str = self.__get_call_url(service=service, endpoint=endpoint)

        # Initializing the parameter variable
        # Will stay empty if the UUID is provided.
        req_params : dict = { }
        
        # If the resource id is provided, it should be appended at the end of the URL
        if(not resource_id is None):
            req_url = f'{req_url}/{resource_id}'
        else:
            if(not filter is None):
                req_params['$filter'] = filter

            if(not select is None):
                req_params['$select'] = select

            if(not orderby is None):
                req_params['$order_by'] = orderby

            if(not search is None):
                req_params['$search'] = search
            
            if(not top is None):
                req_params['$top'] = top

            if(not skip is None):
                req_params['skip'] = skip

            if(not exclude is None):
                req_params['$exclude'] = exclude

        # Making the request
        response : requests.Response = self.__make_request(
            http_method='GET',
            req_url=req_url,
            req_params=req_params,
            req_payload={ },
            req_headers=self.__sc_request_headers
        )
        
        return response
        
    def post(self, service : SCV2Service, endpoint : SCV2BaseEndpoint, payload : dict) -> requests.Response:

        # Validating both Service and Endpoint
        self.__validate_service_endpoint(service=service, endpoint=endpoint)

        # Generating the request URL
        req_url : str = self.__get_call_url(service=service, endpoint=endpoint)

        # Making the request
        response : requests.Response = self.__make_request(
            http_method='POST',
            req_url=req_url,
            req_params={ },
            req_payload=payload,
            req_headers=self.__sc_request_headers
        )

        return response

    def patch(self, service : SCV2Service, endpoint : SCV2BaseEndpoint, resource_id : str, payload : dict, etag : str) -> requests.Response:

        # Validating both Service and Endpoint
        self.__validate_service_endpoint(service=service, endpoint=endpoint)

        # Generating the request URL
        req_url : str = self.__get_call_url(service=service, endpoint=endpoint)

        # For updates, the id  of the resource is appended at the end of the URL
        req_url = f'{req_url}/{resource_id}'

        # Making the request
        response : requests.Response = self.__make_request(
            http_method='PATCH',
            req_url=req_url,
            req_params={ },
            req_payload=payload,
            req_headers={**self.__sc_request_headers, 'If-Match': etag}
        )

        return response

    def put(self, service : SCV2Service, endpoint : SCV2BaseEndpoint, resource_id : str, payload : dict) -> requests.Response:

        # Validating both Service and Endpoint
        self.__validate_service_endpoint(service=service, endpoint=endpoint)

        # Generating the request URL
        req_url : str = self.__get_call_url(service=service, endpoint=endpoint)

        # For updates, the id of the resource is appended at the end of the URL
        if(not resource_id is None and resource_id != ''):
            req_url = f'{req_url}/{resource_id}'

        # Making the request
        response : requests.Response = self.__make_request(
            http_method='PUT',
            req_url=req_url,
            req_params={ },
            req_payload=payload,
            req_headers=self.__sc_request_headers
        )

        return response

    def delete(self, service : SCV2Service, endpoint : SCV2BaseEndpoint, resource_id : str) -> requests.Response:

        # Validating both Service and Endpoint
        self.__validate_service_endpoint(service=service, endpoint=endpoint)

        # Generating the request URL
        req_url : str = self.__get_call_url(service=service, endpoint=endpoint)

        # For delete requests, the resource id should be appended at the end of the request URL
        req_url = f'{req_url}/{resource_id}'

        # Making the request
        response : requests.Response = self.__make_request(
            http_method='DELETE',
            req_url=req_url,
            req_params={ },
            req_payload={ },
            req_headers=self.__sc_request_headers
        )

        return response



    def close(self):
        self.__sc_session.close()

    def from_request(self, request: SCV2Request) -> requests.Response:
        """
        Execute a request created with SCV2RequestBuilder.
        
        Args:
            request: The SCV2Request object to execute
            
        Returns:
            Response from the API
        """
        # Validate the request
        if not isinstance(request, SCV2Request):
            raise ValueError("Expected an SCV2Request object")
            
        # Call the appropriate method based on the request type
        if request.request_type == SCV2RequestType.GET:
            # Extract parameters from the request for GET
            filter_param = request.params.get(SCV2QueryParameterType.FILTER.value)
            select_param = request.params.get(SCV2QueryParameterType.SELECT.value)
            orderby_param = request.params.get(SCV2QueryParameterType.ORDERBY.value)
            search_param = request.params.get(SCV2QueryParameterType.SEARCH.value)
            top_param = request.params.get(SCV2QueryParameterType.TOP.value)
            skip_param = request.params.get(SCV2QueryParameterType.SKIP.value)
            exclude_param = request.params.get(SCV2QueryParameterType.EXCLUDE.value)
            
            return self.get(
                service=request.service,
                endpoint=request.endpoint,
                resource_id=request.resource_id,
                filter=filter_param,
                select=select_param,
                orderby=orderby_param,
                search=search_param,
                top=top_param,
                skip=skip_param,
                exclude=exclude_param
            )
        elif request.request_type == SCV2RequestType.POST:
            return self.post(
                service=request.service,
                endpoint=request.endpoint,
                payload=request.payload
            )
        elif request.request_type == SCV2RequestType.PATCH:
            etag = request.headers.get('If-Match')
            return self.patch(
                service=request.service,
                endpoint=request.endpoint,
                resource_id=request.resource_id,
                payload=request.payload,
                etag=etag
            )
        elif request.request_type == SCV2RequestType.PUT:
            return self.put(
                service=request.service,
                endpoint=request.endpoint,
                resource_id=request.resource_id,
                payload=request.payload
            )
        elif request.request_type == SCV2RequestType.DELETE:
            return self.delete(
                service=request.service,
                endpoint=request.endpoint,
                resource_id=request.resource_id
            )
        else:
            raise ValueError(f"Unsupported request type: {request.request_type}")