class address:
    def __init__(self, address_list, country, state, fax, website):
        for key in address_list:
            if type(address_list[key]) not in [int, str, list, bool]:
                for k in address_list[key]:
                    setattr(self, k, address_list[key][k])
            else:
                if key not in "fax" and key not in "website":
                    setattr(self, key, address_list[key])
        self.country = country
        self.state = state
        self.fax = fax
        self.website = website
