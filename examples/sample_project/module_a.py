"""Module A - Data Processing"""


def process_data(data):
    """Process input data"""
    return [x * 2 for x in data]


def validate_data(data):
    """Validate input data"""
    return all(isinstance(x, (int, float)) for x in data)


class DataProcessor:
    """Main data processor class"""
    
    def __init__(self, multiplier=2):
        self.multiplier = multiplier
    
    def process(self, data):
        """Process data with multiplier"""
        return [x * self.multiplier for x in data]
