from src.config import Config
from src.main import app


class TestMain:
    def test_main_successful(self) -> None:
        assert app.title == Config.APP.TITLE
        assert app.description == Config.APP.DESCRIPTION
        assert app.version == Config.APP.VERSION
