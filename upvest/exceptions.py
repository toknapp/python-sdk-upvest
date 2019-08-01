class InvalidRequest(Exception):
    def __init__(self, response):
        self.response = response
