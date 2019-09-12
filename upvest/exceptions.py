class InvalidRequest(Exception):
    def __init__(self, response):
        self.response = response


class RecoveryFailedError(Exception):
    pass


class AuthenticationError(Exception):
    pass
