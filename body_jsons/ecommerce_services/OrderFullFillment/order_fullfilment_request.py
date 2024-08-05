class order_fullfillment_request:
    def __init__(self, storeKey, orderId, items, trackingNumbers):
        self.storeKey = storeKey
        self.orderId = orderId
        self.items = items
        self.trackingNumbers = trackingNumbers
