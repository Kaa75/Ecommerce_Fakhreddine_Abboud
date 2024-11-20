from supabase import Client
from src.base import get_unauthenticated_client
from pydantic import BaseModel

class Inventory(BaseModel):
    name: str = ""
    location: str = ""
    id: int= -1

def run():
    client = get_unauthenticated_client()
    # s = client.table("Inventory").insert({"name":"abboud", "location":"USA"}).execute()
    t = client.table("Inventory").select("*").execute()
    
    print(t)