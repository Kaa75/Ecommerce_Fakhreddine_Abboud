import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    class APP:
        TITLE = "Ecommerce Abboud Fakhreddine 435L"
        DESCRIPTION = "Welcome to the Ecommerce Karim Abboud Rayan Fakhreddine 435L API"
        VERSION = "0.1.0"

    class SUPABASE:
        KEY = os.getenv("SUPABASE_KEY")
        URL = os.getenv("SUPABASE_URL")

    class JWT:
        SECRET = os.getenv("JWT_SECRET")
        ALGORITHM = "HS256"
        AUDIENCE = "authenticated"

    class Testing:
        class RANDOM:
            SEED = 0
