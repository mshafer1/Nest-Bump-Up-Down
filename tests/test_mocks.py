
class Device(object):
    def __init__(self):
        self.hvac_state = ''
        self.target = 0 # can be a tuple
        self.temperature = 0
        self.mode = ''
