

class CommenceNotInstalled(Exception):
    def __init__(self, msg="Commence is not installed"):
        self.msg = msg
        super().__init__(self.msg)
