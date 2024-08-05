class state:
    def __init__(self, state_dict):
        for key in state_dict:
            setattr(self, key, state_dict[key])
