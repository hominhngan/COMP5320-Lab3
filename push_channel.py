"""Exercise 2: add a notification strategy without editing TaskService."""

class PushChannel:
    def __init__(self):
        self.sent = []

    def send(self, recipient: str, message: str) -> None:
        # Record the accepted request as a (recipient, message) tuple.
        # This is a local simulation; do not call a real push provider.
        raise NotImplementedError('Complete exercise 2')
