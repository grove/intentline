class IntentlineError(Exception):
    """A diagnosed input or storage failure."""

    def __init__(self, message, code=2):
        super().__init__(message)
        self.code = code
