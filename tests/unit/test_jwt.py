from app.utils import create_token
from app.utils import get_jwt_payload


class TestToken:
    def test_creating(self):
        access_token = create_token("access", 5)
        assert isinstance(access_token, str)
        assert access_token.count(".") == 2

    def test_payload(self):
        access_token = create_token("access", 5)
        payload = get_jwt_payload(access_token)
        assert int(payload["sub"]) == 5
        assert payload["type"] == "access_token"
