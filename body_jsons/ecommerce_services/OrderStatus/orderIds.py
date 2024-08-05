class orderIds:
    def __init__(self, orderId_dict):
        for key in orderId_dict:
            setattr(self, key, orderId_dict[key])
