import os
from supabase import create_client, Client

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

class ClientSupabase:
    def __init__(self):
        self.supabase: Client = create_client(url, key)

    def save_purchase(self, data):
        try:
            response = self.supabase.table("purchases").insert(data).execute()
            return response
        except Exception as exception:
            print(exception)
            return exception
        
    def save_sell(self, data):
        try:
            response = self.supabase.table("sell").insert(data).execute()
            return response
        except Exception as exception:
            print(exception)
            return exception