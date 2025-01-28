from app.utils import get_password_hash, verify_password


class TestPswdUtils:
    def test_generate_hash(self):
        assert get_password_hash("123") != "123"

    def test_verifying_password(self):
        assert verify_password("123", get_password_hash("123"))
