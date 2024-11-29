import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings for the Ecommerce application."""
    
    class APP:
        """Application-level settings."""
        TITLE = "Ecommerce Abboud Fakhreddine 435L"
        DESCRIPTION = "Welcome to the Ecommerce Karim Abboud Rayan Fakhreddine 435L API"
        VERSION = "0.1.0"

    class SUPABASE:
        """Supabase configuration settings."""
        KEY = os.getenv("SUPABASE_KEY")
        URL = os.getenv("SUPABASE_URL")

    class JWT:
        """JWT authentication settings."""
        SECRET = os.getenv("JWT_SECRET")
        ALGORITHM = "HS256"
        AUDIENCE = "authenticated"

    class Testing:
        """Testing configurations."""
        
        class RANDOM:
            """Randomization settings for testing."""
            SEED = 0
