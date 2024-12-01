from src.config import Config


class TestConfig:
    class TestApp:
        def test_app(self) -> None:
            assert Config.APP.TITLE == "Ecommerce Abboud Fakhreddine 435L"
            assert Config.APP.DESCRIPTION == "Welcome to the Ecommerce Karim Abboud Rayan Fakhreddine 435L API"
            assert Config.APP.VERSION == "0.1.0"

    class TestSupabase:
        def test_supabase(self) -> None:
            Config.SUPABASE.KEY = "SUPABASE_KEY"
            Config.SUPABASE.URL = "SUPABASE_URL"
            assert Config.SUPABASE.KEY == "SUPABASE_KEY"
            assert Config.SUPABASE.URL == "SUPABASE_URL"

    class TestJWT:
        def test_jwt(self) -> None:
            Config.JWT.SECRET = "JWT_SECRET"
            assert Config.JWT.SECRET == "JWT_SECRET"
            assert Config.JWT.ALGORITHM == "HS256"
            assert Config.JWT.AUDIENCE == "authenticated"

    class TestTesting:
        class TestRandom:
            def test_random(self) -> None:
                assert Config.Testing.RANDOM.SEED == 0
