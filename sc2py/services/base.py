from enum import Enum

class SCV2Service(Enum):
    """
    Enumeration of available SAP Sales/Service Cloud V2 API services.
    """
    SALES_TERRITORY_SERVICE = 'sales-territory-service'
    UTILITIES_COLLECTION_SERVICE = 'collections-integration-service'
    CONTACT_PERSON_SERVICE = 'contact-person-service'
    ORGANIZATIONAL_UNIT_SERVICE = 'organizational-unit-service'
    # Add more services as they become available

class SCV2BaseEndpoint(Enum):
    """
    Base class for service-specific endpoint enumerations.
    This is used for type checking but doesn't contain actual endpoints.
    """
    pass