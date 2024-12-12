from jwt import decode, InvalidTokenError


def decode_hs256(token: str, client_id: str, client_secret: str):
    try:
        if not isinstance(token, bytes):
            token = token.encode('utf-8')  # 必要に応じてエンコード
        decoded_token = decode(
            jwt=token,
            key=client_secret,
            algorithms=["HS256"],
            audience=client_id
        )
        return decoded_token
    except InvalidTokenError as e:
        raise ValueError(f"トークンの検証に失敗しました: {str(e)}")
