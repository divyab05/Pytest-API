class storedetails:
    def __init__(self, storedetails_list):
        for key in storedetails_list:
            setattr(self, key, storedetails_list[key])
