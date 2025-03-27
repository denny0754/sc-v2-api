from enum import Enum

class SCV2Service(Enum):
    """
    Enumeration of available SAP Sales/Service Cloud V2 API services.
    """
    SALES_TERRITORY_SERVICE = 'sales-territory-service'

    UTILITIES_COLLECTION_SERVICE = 'collections-integration-service'

    CONTACT_PERSON_SERVICE = 'contact-person-service'

    ORGANIZATIONAL_UNIT_SERVICE = 'organizational-unit-service'

    ACCOUNT_HIERARCHY_SERVICE = 'account-hierarchy-service'

    ACCOUNT_SERVICE = 'account-service'

    ACTIVITY_ASSIGNMENT_RULE_SERVICE = 'activity-assignment-rule-service'

    ACTIVITY_PLAN_SERVICE = 'activity-plan-service'

    APPOINTMENT_SERVICE = 'appointment-service'

    CASE_SERVICE = 'case-service'

    COMPETITOR_PRODUCT_SERVICE = 'competitor-product-service'

    DOCUMENT_SERVICE = 'document-service'

    EMPLOYEE_SERVICE = 'employee-service'

    FUNCTIONAL_LOCATION_SERVICE = 'functional-location-service'

    INDIVIDUAL_CUSTOMER_SERVICE = 'individual-customer-service'

    INSTALL_BASE_SERVICE = 'installed-base-service'

    CHAT_SERVICE = 'chat-service'

    INTERACTION_EMAIL_SERVICE = 'email-service'

    INTERACTION_PHONE_SERVICE = 'phone-service'

    LEAD_SERVICE = 'lead-service'

    OPPORTUNITY_SERVICE = 'opportunity-service'

    PRODUCT_GROUP_SERVICE = 'product-group-service'

    PRODUCT_SERVICE = 'product-service'

class SCV2BaseEndpoint(Enum):
    """
    Base class for service-specific endpoint enumerations.
    This is used for type checking but doesn't contain actual endpoints.
    """
    pass