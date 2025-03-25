from sc2py.services import SCV2Service, SCV2BaseEndpoint

class SCV2BatchRequestBuilder:

    __sc_request : dict = { }

    def __init__(self):
        self.__sc_request = {
            'http_method': None,
            'sc_service': None,
            'sc_endpoint': None,
            'sc_resource_id': None,
            'sc_params': {},
            'sc_payload': None,
            'sc_headers': {}
        }

    def __set_request_details(self, http_method : str, service : SCV2Service, endpoint : SCV2BaseEndpoint):
        self.__sc_request['http_method'] = http_method
        self.__sc_request['sc_service'] = service
        self.__sc_request['sc_endpoint'] = endpoint

    def get(self, service : SCV2Service, endpoint : SCV2BaseEndpoint) -> "SCV2BatchRequestBuilder":
        self.__set_request_details(
            http_method='GET',
            service=service,
            endpoint=endpoint
        )
        return self

    def post(self, service : SCV2Service, endpoint : SCV2BaseEndpoint) -> "SCV2BatchRequestBuilder":
        self.__set_request_details(
            http_method='POST',
            service=service,
            endpoint=endpoint
        )
        return self

    def patch(self, service : SCV2Service, endpoint : SCV2BaseEndpoint) -> "SCV2BatchRequestBuilder":
        self.__set_request_details(
            http_method='PATCH',
            service=service,
            endpoint=endpoint
        )
        return self

    def put(self, service : SCV2Service, endpoint : SCV2BaseEndpoint) -> "SCV2BatchRequestBuilder":
        self.__set_request_details(
            http_method='PUT',
            service=service,
            endpoint=endpoint
        )
        return self

    def delete(self, service : SCV2Service, endpoint : SCV2BaseEndpoint) -> "SCV2BatchRequestBuilder":
        self.__set_request_details(
            http_method='DELETE',
            service=service,
            endpoint=endpoint
        )
        return self

    def with_resource_id(self, resource_id : str) -> "SCV2BatchRequestBuilder":
        self.__sc_request['resource_id'] = resource_id
        return self

    def with_param(self, key : str, value : str) -> "SCV2BatchRequestBuilder":
        self.__sc_request['sc_params'][key] = value
        return self
    
    def build(self):
        # Validate the configuration
        if not self.__sc_request['http_method']:
            raise ValueError("HTTP method is required")
        
        return self.__sc_request

class SCV2ClientBatchRequest:

    __sc_requests : list

    __sc_requests_ids : dict

    def __init__(self):
        self.__sc_requests = []
        self.__sc_requests_ids = { }

    def __add_request_id(self, request_id : str):
        if(request_id in self.__sc_requests_ids):
            raise ValueError(f"Request ID '{request_id}' is already in use")

        self.__sc_requests_ids[request_id] = len(self.__sc_requests) - 1

    def __validate_request_params(self, request_id : str, service : SCV2Service, endpoint : SCV2BaseEndpoint):
        if not request_id:
            raise ValueError("Request ID cannot be empty")
    
        if not service or not endpoint:
            raise ValueError("Service and endpoint must be provided")

    def add_get_request(self,
            request_id : str,
            service : SCV2Service,
            endpoint : SCV2BaseEndpoint,
            priority : int = 0,
            resource_id : str = None,
            filter : str = None,
            select : str = None,
            orderby : str = None,
            search : str = None,
            top : int = None,
            skip : int = None,
            exclude : str = None) -> "SCV2ClientBatchRequest":
        
        self.__validate_request_params(request_id=request_id, service=service, endpoint=endpoint)

        # Excluding all None parameters
        sc_params : dict = {k: v for k, v in {
            '$filter': filter,
            '$select': select,
            '$orderby': orderby,
            '$search': search,
            '$top': top,
            '$skip': skip,
            '$exclude': exclude
        }.items() if v is not None}

        self.__sc_requests.append({
            '_id': request_id,
            '_priority': priority,
            'http_method': 'GET',
            'sc_service': service,
            'sc_endpoint': endpoint,
            'sc_resource_id': resource_id,
            'sc_params': sc_params,
            'sc_payload': None,
            'sc_headers': { }
        })

        self.__add_request_id(request_id=request_id)

        return self
    
    def add_post_request(self, request_id : str, service : SCV2Service, endpoint : SCV2BaseEndpoint, payload : dict, priority : int = 0) -> "SCV2ClientBatchRequest":
        
        self.__validate_request_params(request_id=request_id, service=service, endpoint=endpoint) 

        if not payload:
            raise ValueError(f"Payload is required for POST request '{request_id}'")

        self.__sc_requests.append({
            '_id': request_id,
            '_priority': priority,
            'http_method': 'POST',
            'sc_service': service,
            'sc_endpoint': endpoint,
            'sc_resource_id': None,
            'sc_params': None,
            'sc_payload': payload,
            'sc_headers': { }
        })

        self.__add_request_id(request_id=request_id)

        return self
    
    def add_patch_request(self,
                          request_id : str,
                          service : SCV2Service,
                          endpoint : SCV2BaseEndpoint,
                          resource_id : str,
                          payload : dict,
                          etag : str,
                          priority : int = 0) -> "SCV2ClientBatchRequest":

        self.__validate_request_params(request_id=request_id, service=service, endpoint=endpoint)

        if not resource_id:
            raise ValueError(f"Resource ID is required for PATCH request '{request_id}'")
            
        if not payload:
            raise ValueError(f"Payload is required for PATCH request '{request_id}'")
            
        if not etag:
            raise ValueError(f"ETag is required for PATCH request '{request_id}'")

        self.__sc_requests.append({
            '_id': request_id,
            '_priority': priority,
            'http_method': 'PATCH',
            'sc_service': service,
            'sc_endpoint': endpoint,
            'sc_resource_id': resource_id,
            'sc_params': None,
            'sc_payload': payload,
            'sc_headers': { 'If-Match': etag }
        })

        self.__add_request_id(request_id=request_id)

        return self
    
    def add_put_request(self, request_id : str, service : SCV2Service, endpoint : SCV2BaseEndpoint, resource_id : str, payload : dict, priority : int = 0) -> "SCV2ClientBatchRequest":
        
        self.__validate_request_params(request_id=request_id, service=service, endpoint=endpoint)

        self.__sc_requests.append({
            '_id': request_id,
            '_priority': priority,
            'http_method': 'PUT',
            'sc_service': service,
            'sc_endpoint': endpoint,
            'sc_resource_id': resource_id,
            'sc_params': None,
            'sc_payload': payload,
            'sc_headers': { }
        })

        self.__add_request_id(request_id=request_id)

        return self

    def add_delete_request(self, request_id : str, service : SCV2Service, endpoint : SCV2BaseEndpoint, resource_id : str, priority : int = 0) -> "SCV2ClientBatchRequest":
        
        self.__validate_request_params(request_id=request_id, service=service, endpoint=endpoint)

        self.__sc_requests.append({
            '_id': request_id,
            '_priority': priority,
            'http_method': 'DELETE',
            'sc_service': service,
            'sc_endpoint': endpoint,
            'sc_resource_id': resource_id,
            'sc_params': None,
            'sc_payload': None,
            'sc_headers': { }
        })

        self.__add_request_id(request_id=request_id)

        return self

    def add_dependent_request(self,
                            request_id: str,
                            depends_on: str,
                            transform_function: callable,
                            priority: int = 0) -> "SCV2ClientBatchRequest":
        """
        Add a request that depends on the result of a previous request.
        
        This allows you to create requests that need data from earlier responses.
        The transform_function receives the parent request's response and must
        return a dictionary with the configuration for the dependent request.
        
        Args:
            request_id: Unique identifier for this request
            depends_on: ID of the parent request this one depends on
            transform_function: Function that takes the parent response and
                                returns a request configuration dictionary
            priority: Request priority (higher numbers = higher priority)
                            
        Returns:
            Self reference for method chaining
            
        Example:
            def transform_func(parent_response):
                account_id = parent_response.json()['id']
                return {
                    'http_method': 'GET',
                    'sc_service': SCV2Service.CONTACTS,
                    'sc_endpoint': SCV2BaseEndpoint.COLLECTION,
                    'sc_params': {'$filter': f"accountId eq '{account_id}'"}
                }
                
            batch.add_get_request("get_account", ...)
                .add_dependent_request("get_contacts", 
                                    depends_on="get_account",
                                    transform_function=transform_func)
        """
        # Check if the request ID is already in use
        if request_id in self.__sc_requests_ids:
            raise ValueError(f"Request ID '{request_id}' is already in use")
        
        # Check if the parent request exists
        if depends_on not in self.__sc_requests_ids:
            raise ValueError(f"Parent request '{depends_on}' not found")
            
        # Check if the transform function is callable
        if not callable(transform_function):
            raise ValueError("Transform function must be callable")
        
        # Add the dependent request to the batch
        self.__sc_requests.append({
            '_id': request_id,
            '_priority': priority,
            'is_dependent': True,
            'depends_on': depends_on,
            'transform_function': transform_function
        })
        
        # Register the request ID
        self.__add_request_id(request_id=request_id)
        
        return self

    def remove_request(self, request_id : str) -> "SCV2ClientBatchRequest":
        """
        Remove a request from the batch.
        
        Args:
            request_id: The ID of the request to remove
            
        Returns:
            Self reference for method chaining
        """
        if request_id in self.__sc_requests_ids:
            idx = self.__sc_requests_ids[request_id]
            self.__sc_requests.pop(idx)
            
            # Rebuild the request ID mapping
            self.__sc_requests_ids = {}
            for i, req in enumerate(self.__sc_requests):
                self.__sc_requests_ids[req['_id']] = i
        
        return self

    def get_requests(self):
        return self.__sc_requests