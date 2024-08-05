class onboard_magento1:
    def __init__(self, apiUrl, accessToken, storesDetails, warehouses, message):
        self.apiUrl = apiUrl
        self.accessToken = accessToken
        self.message = message
        self.storesDetails = storesDetails
        self.warehouses = warehouses
