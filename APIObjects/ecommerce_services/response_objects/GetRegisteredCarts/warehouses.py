class warehouses:
    def __init__(self, warehouse_dict, address):
        for key in warehouse_dict:
            setattr(self, key, warehouse_dict[key])
        self.address = address
