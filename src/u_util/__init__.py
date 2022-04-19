def execute(func, msg, *arg, **karg):
    """ informing user before and after executing function """
    print(msg, end=" ", flush=True)
    func(*arg, **karg)
    print("Done")


def b64_to_byte(msg: str) -> bytes:
    """ encode string to bytes based on base64 """
    import base64
    return base64.b64decode(msg)


def byte_to_b64(cipher: bytes) -> str:
    """ decode bytes to string based on base64 """
    import base64
    return str(base64.b64encode(cipher))


def encode_jwt_token(payload: dict, key: bytes) -> str:
    """ encrypt payload to jwt token """
    import jwt
    return jwt.encode(payload, key, algorithm = "HS256")


def decode_jwt_token(token: str, key: bytes) -> dict:
    """ decrypt payload from token """
    import jwt
    try:
        payload = jwt.decode(token, key)
        return payload
    except jwt.ExpiredSignatureError:
        return {}
    except jwt.InvalidTokenError:
        return {}
