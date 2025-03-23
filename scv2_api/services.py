from enum import Enum
from typing import Type, Dict, Any, Generic, TypeVar

class SCV2Service(Enum):
    SALES_TERRITORY_SERVICE = 'sales-territory-service'

    UTILITIES_COLLECTION_SERVICE = 'collections-integration-service'

    CONTACT_PERSON_SERVICE = 'contact-person-service'

    ORGANIZATIONAL_UNIT_SERVICE = 'organizational-unit-service'

class SCV2BaseEndpoint(Enum): pass

class SalesTerritoryServiceEndpoint(SCV2BaseEndpoint):
    SALES_TERRITORIES       = 'sales-territories'

class CollectionsIntegrationServiceEndpoint(SCV2BaseEndpoint):
    CORRESPONDENCE_HISTORY  = 'correspondenceHistory'
    DUNNING                 = 'dunning'
    RETURNS                 = 'returns'
    WRITE_OFF               = 'writeOff'

class ContactPersonServiceEndpoint(SCV2BaseEndpoint):
    CONTACT_PERSONS = 'contactPersons'

class OrganizationalUnitServiceEndpoint(SCV2BaseEndpoint):
    DISTRIBUTION_CHANNEL = 'distributionChannels'
    DIVISION = 'divisions'
    ORGANIZATIONAL_UNIT = 'organizationalUnits'

class InternalAPIEndpointSanitizer:

    __SERVICE_ENDPOINT_MAP : Dict[SCV2Service, Type[SCV2BaseEndpoint]] = {
        SCV2Service.SALES_TERRITORY_SERVICE : SalesTerritoryServiceEndpoint,
        SCV2Service.UTILITIES_COLLECTION_SERVICE : CollectionsIntegrationServiceEndpoint,
        SCV2Service.CONTACT_PERSON_SERVICE : ContactPersonServiceEndpoint,
        SCV2Service.ORGANIZATIONAL_UNIT_SERVICE : OrganizationalUnitServiceEndpoint
    }

    @staticmethod
    def is_valid_endpoint(service : SCV2Service, endpoint : SCV2BaseEndpoint) -> bool:
        return isinstance(endpoint, InternalAPIEndpointSanitizer.__SERVICE_ENDPOINT_MAP[service])
