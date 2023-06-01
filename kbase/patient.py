class Patient:
    def __init__(self, data={}):
        self.data = data

    # Define each field of the data as a dictionary key
    # This allows us to access the data by name
    def get(self, field):
        return self.data[field]
    
    def set(self, field, value):
        self.data[field] = value
