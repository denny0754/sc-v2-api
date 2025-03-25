from typing import Type, Dict

from scv2_api.services import *

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