class country:
    def __init__(self, country_dict):
        for key in country_dict:
            setattr(self, key, country_dict[key])
