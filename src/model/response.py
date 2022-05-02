class Response:
    def __init__(self, code: int, msg: str = None, resp = None):
        self.code = code
        self.msg = msg
        self.resp = resp

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "resp": self.resp
        }
