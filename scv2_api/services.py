from enum import Enum
from typing import Type, Dict, Any, Generic, TypeVar

class SalesCloudAPIService(Enum):
    SALES_TERRITORY_SERVICE = 'sales-territory-service'

    UTILITIES_COLLECTION_SERVICE = 'collections-integration-service'

    CONTACT_PERSON_SERVICE = 'contact-person-service'

    ORGANIZATIONAL_UNIT_SERVICE = 'organizational-unit-service'

class BaseEndpoint(Enum): pass

class SalesTerritoryServiceEndpoint(BaseEndpoint):
    SALES_TERRITORIES       = 'sales-territories'

class CollectionsIntegrationServiceEndpoint(BaseEndpoint):
    CORRESPONDENCE_HISTORY  = 'correspondenceHistory'
    DUNNING                 = 'dunning'
    RETURNS                 = 'returns'
    WRITE_OFF               = 'writeOff'

class ContactPersonServiceEndpoint(BaseEndpoint):
    CONTACT_PERSONS = 'contactPersons'

class OrganizationalUnitServiceEndpoint(BaseEndpoint):
    DISTRIBUTION_CHANNEL = 'distributionChannels'
    DIVISION = 'divisions'
    ORGANIZATIONAL_UNIT = 'organizationalUnits'

class InternalAPIEndpointSanitizer:

    __SERVICE_ENDPOINT_MAP : Dict[SalesCloudAPIService, Type[BaseEndpoint]] = {
        SalesCloudAPIService.SALES_TERRITORY_SERVICE : SalesTerritoryServiceEndpoint,
        SalesCloudAPIService.UTILITIES_COLLECTION_SERVICE : CollectionsIntegrationServiceEndpoint,
        SalesCloudAPIService.CONTACT_PERSON_SERVICE : ContactPersonServiceEndpoint,
        SalesCloudAPIService.ORGANIZATIONAL_UNIT_SERVICE : OrganizationalUnitServiceEndpoint
    }

    @staticmethod
    def is_valid_endpoint(service : SalesCloudAPIService, endpoint : BaseEndpoint) -> bool:
        return isinstance(endpoint, InternalAPIEndpointSanitizer.__SERVICE_ENDPOINT_MAP[service])
