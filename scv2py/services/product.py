from scv2py.services.base import SCV2BaseEndpoint

class ProductServiceEndpoint(SCV2BaseEndpoint):
    """
    Endpoints available in the Product Service.
    """
    PRODUCT = 'products'

    SALES_STATUS = 'salesStatus'

    TYPE = 'productTypes'

    UNIT_OF_MEASURE = 'unitOfMeasures'