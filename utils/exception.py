class EmailFormatException(Exception):

    def __init__(self, value):
        self.error_message = value


class MobileNumberLengthException(Exception):

    def __init__(self, value):
        self.error_message = value


class MobileNumberFormatException(Exception):

    def __init__(self, value):
        self.error_message = value


class UserNameAlreadyTakenException(Exception):

    def __init__(self, value):
        self.error_message = value


class UserNameLengthException(Exception):

    def __init__(self, value):
        self.error_message = value


class AccountAlreadyExist(Exception):

    def __init__(self, value):
        self.error_message = value


class PasswordLengthException(Exception):

    def __init__(self, value):
        self.error_message = value
