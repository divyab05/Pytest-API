class cartList:
    def __init__(self, cart_list_dict):
        for key in cart_list_dict:
            setattr(self, key, cart_list_dict[key])
