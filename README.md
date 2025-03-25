# SCV2 API

A modern Python wrapper for the SAP Sales and Service Cloud V2 API that simplifies making API requests while providing powerful features like client-side batching and request dependencies.

## About

This library provides:

- Secure authentication with persistent sessions
- Intuitive methods for all HTTP operations
- Client-side batching for concurrent requests
- Request dependencies for complex workflows
- Robust error handling with specific exception types

## Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/scv2_api.git
cd scv2_api
```

Then install using:

```bash
pip install -e .
```

## Quick Start

```python
from scv2_api import SCV2Session
from scv2_api import SCV2Service, ContactPersonServiceEndpoint

# Create a session with your credentials
with SCV2Session(
    sc_host="my1122334.de1.test.crm.cloud.sap",
    sc_user="your_username",
    sc_password="your_password"
) as session:
    
    # Make a simple GET request to retrieve contact persons
    response = session.get(
        service=SCV2Service.CONTACT_PERSON_SERVICE,
        endpoint=ContactPersonServiceEndpoint.CONTACT_PERSONS,
        top=10
    )
    
    # Process the response
    contacts = response.json()
    for contact in contacts:
        print(f"Contact: {contact['fullName']}")
```

## Working with Batch Requests

For improved performance, use client-side batching to execute multiple requests concurrently:

```python
from scv2_api import SCV2ClientBatchRequest
from scv2_api import SCV2Service, ContactPersonServiceEndpoint, OrganizationalUnitServiceEndpoint

# Create a batch request
batch = SCV2ClientBatchRequest()

# Add multiple requests to the batch
batch.add_get_request(
    request_id="get_organizational_units",
    service=SCV2Service.ORGANIZATIONAL_UNIT_SERVICE,
    endpoint=OrganizationalUnitServiceEndpoint.ORGANIZATIONAL_UNIT,
    top=10
)

batch.add_get_request(
    request_id="get_contacts",
    service=SCV2Service.CONTACT_PERSON_SERVICE,
    endpoint=ContactPersonServiceEndpoint.CONTACT_PERSONS,
    top=10
)

# Execute the batch (requests run concurrently)
results = session.execute_batch(batch)

# Process results
if results["get_organizational_units"]["success"]:
    org_units = results["get_organizational_units"]["response"].json()
    print(f"Retrieved {len(org_units)} organizational units")

if results["get_contacts"]["success"]:
    contacts = results["get_contacts"]["response"].json()
    print(f"Retrieved {len(contacts)} contacts")
```

## Request Dependencies

When subsequent requests need data from previous ones, use dependent requests:

```python
# Add a request to get a specific organizational unit
batch.add_get_request(
    request_id="get_org_unit",
    service=SCV2Service.ORGANIZATIONAL_UNIT_SERVICE,
    endpoint=OrganizationalUnitServiceEndpoint.ORGANIZATIONAL_UNIT,
    resource_id="12345"
)

# Add a dependent request to get related contact persons
def get_org_unit_contacts(org_unit_response):
    org_unit = org_unit_response.json()
    org_unit_id = org_unit['id']
    
    # Build a request based on the organizational unit ID
    builder = SCV2RequestBuilder()
    return (
        builder.get(SCV2Service.CONTACT_PERSON_SERVICE, ContactPersonServiceEndpoint.CONTACT_PERSONS)
               .filter(f"organizationalUnitId eq '{org_unit_id}'")
               .build()
    )

batch.add_dependent_request(
    request_id="get_contacts_for_org_unit",
    depends_on="get_org_unit",
    transform_function=get_org_unit_contacts
)
```

## Advanced Request Building

The `SCV2RequestBuilder` isn't just for dependent requests. You can use it to create any request with a fluent interface:

```python
from scv2_api import SCV2RequestBuilder, SCV2Session
from scv2_api import SCV2Service, SalesTerritoryServiceEndpoint

# Create a session
with SCV2Session(
    sc_host="my1122334.de1.test.crm.cloud.sap",
    sc_user="your_username",
    sc_password="your_password"
) as session:
    
    # Create a builder for a complex query
    builder = SCV2RequestBuilder()
    
    # Build the request with a fluent interface
    request = (
        builder.get(SCV2Service.SALES_TERRITORY_SERVICE, SalesTerritoryServiceEndpoint.SALES_TERRITORIES)
               .filter("country eq 'Germany' and active eq true")
               .select(["id", "name", "country", "region"])
               .orderby("name asc")
               .top(50)
               .build()
    )
    
    # Execute the request
    response = session.from_request(request)
    
    # Process the response
    territories = response.json()
    print(f"Found {len(territories)} sales territories in Germany")
```

## Available Services

The library currently supports the following SAP Sales/Service Cloud V2 API services:

- `SCV2Service.SALES_TERRITORY_SERVICE` - Sales territory management
  - `SalesTerritoryServiceEndpoint.SALES_TERRITORIES` - Access sales territories

- `SCV2Service.UTILITIES_COLLECTION_SERVICE` - Collections integration service
  - `CollectionsIntegrationServiceEndpoint.CORRESPONDENCE_HISTORY` - Access correspondence history
  - `CollectionsIntegrationServiceEndpoint.DUNNING` - Manage dunning processes
  - `CollectionsIntegrationServiceEndpoint.RETURNS` - Handle returns
  - `CollectionsIntegrationServiceEndpoint.WRITE_OFF` - Manage write-offs

- `SCV2Service.CONTACT_PERSON_SERVICE` - Contact person management
  - `ContactPersonServiceEndpoint.CONTACT_PERSONS` - Access contact persons

- `SCV2Service.ORGANIZATIONAL_UNIT_SERVICE` - Organizational unit management
  - `OrganizationalUnitServiceEndpoint.DISTRIBUTION_CHANNEL` - Access distribution channels
  - `OrganizationalUnitServiceEndpoint.DIVISION` - Access divisions
  - `OrganizationalUnitServiceEndpoint.ORGANIZATIONAL_UNIT` - Access organizational units

## API Reference

### Core Components

- `SCV2Session` - Main class for API interactions with methods for all HTTP operations
- `SCV2Request` and `SCV2RequestBuilder` - For building requests with a fluent interface
- `SCV2ClientBatchRequest` - Builds and manages batches of requests for concurrent execution

### Exception Types

- `SCV2ConnectionError` - Network connectivity issues
- `SCV2TimeoutError` - Request timeout issues
- `SCV2RequestError` - General request errors
- `SCV2InvalidEndpointException` - Invalid service/endpoint combinations

## Error Handling

The library provides several custom exception types:

```python
try:
    response = session.get(
        service=SCV2Service.CONTACT_PERSON_SERVICE,
        endpoint=ContactPersonServiceEndpoint.CONTACT_PERSONS
    )
except SCV2ConnectionError as e:
    print(f"Connection error: {e}")
except SCV2TimeoutError as e:
    print(f"Request timed out: {e}")
except SCV2RequestError as e:
    print(f"Request error: {e}")
except SCV2InvalidEndpointException as e:
    print(f"Invalid endpoint: {e}")
```

## Compatibility

- Python 3.9+
- Works with SAP Sales and Service Cloud V2 API

## Current Features

Features already implemented in this library:

- **Core API Wrapper**: Complete wrapper for the SAP Sales/Service Cloud V2 API
- **Fluent Request Builder**: Builder pattern for constructing complex API requests
- **Service-Specific Endpoints**: Structured organization of services and endpoints
- **Client-Side Batching**: Execute multiple requests concurrently
- **Request Dependencies**: Chain requests with dependencies on previous results
- **Robust Error Handling**: Specific exception types for different error scenarios
- **Session Management**: Persistent session handling with connection pooling
- **Context Manager Support**: Use the library with Python's `with` statement
- **Comprehensive Parameter Support**: OData query parameters with dedicated methods

## Roadmap

Future planned enhancements for this library:

- **Additional Services**: Expand support for more SAP Sales/Service Cloud V2 API services as they become available
- **Response Models**: Type-hinted response models for better developer experience
- **Pagination Helpers**: Automatic handling of paginated responses
- **Retry Mechanisms**: Intelligent retry logic for failed requests
- **Webhooks**: Support for webhook implementation
- **CLI Tool**: Command-line interface for quick API interactions
- **PyPI Release**: Make the package installable via pip
- **Type-Safe Entity Models**: Pydantic models representing service entities for validation and serialization
- **Async Support**: Async versions of API methods using aiohttp or httpx for non-blocking operations
- **Response Caching**: LRU caching with configurable TTL for frequently requested data
- **Export/Import Functionality**: Tools to help users export/import data between environments
- **Schema Discovery**: Methods to programmatically discover available fields and relationships
- **Mock API Mode**: Testing mode that simulates API responses without making real calls
- **Bulk Data Operations**: Tools for efficiently loading/updating large datasets
- **Change Tracking**: Features to detect and reconcile changes between local objects and remote API state
- **Automatic ETag Management**: Streamlined handling of ETags for optimistic concurrency control
- **Data Validation Helpers**: Functions to validate data against API constraints before sending requests
- **Framework Integrations**: Adapters for Django, FastAPI, Flask to simplify integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
