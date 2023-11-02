from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
import os
from pydantic import BaseModel

class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = FastAPI()

@app.get("/")
def home():
    return "Home page"

@app.get("/health/")
def health():
    return {"status": "ok"}

@app.get("/cats/")
def get_cats():
    response = supabase.table('cat_breeds').select("breed").execute()
    return response

@app.get("/todo/")
async def get_items():
    response = supabase.table('todos').select("*").execute()
    return response

@app.post("/todo/")
async def add_item(item: TodoItem):
    data, count = supabase.table('todos').insert(item.dict()).execute()
    return {"status": "ok", "message": "Item added", "data": data, "count": count}

@app.put("/todo/{item_id}")
async def edit_item(item_id: int, request: dict):
    response = supabase.table('todos').update(request).eq('id', item_id).execute()
    return response

@app.delete("/todo/{item_id}")
async def delete_item(item_id: int):
    response = supabase.table('todos').delete().eq('id', item_id).execute()
    return response

@app.get("/domains/")
def check_domains():
    domains = [
        'https://juanjaramillo.tech',
        'https://testing.juanjaramillo.tech',
        'https://blog.juanjaramillo.tech',
        'https://shop.juanjaramillo.tech',
        'https://api.juanjaramillo.tech'
    ]
    health_status = {}
    for domain in domains:
        try:
            response = requests.get(domain)
            if response.status_code == 200:
                health_status[domain] = "Healthy"
            else:
                health_status[domain] = f"Unhealthy - {response.status_code}"
        except Exception as e:
            health_status[domain] = f"Error - {str(e)}"
    return health_status