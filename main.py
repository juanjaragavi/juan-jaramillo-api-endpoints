from fastapi import FastAPI
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
import os

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

todo_items = []

@app.get("/todo/")
def get_items():
    return {"items": todo_items}

@app.post("/todo/")
def add_item(request: dict):
    todo_items.append(request["item"])
    return {"status": "ok", "message": "Item added"}

@app.put("/todo/{item_index}")
def edit_item(item_index: int, request: dict):
    try:
        todo_items[item_index] = request["new_title"]
        return {"status": "ok", "message": f"Item at index {item_index} updated"}
    except IndexError:
        return {"status": "error", "message": "Item index out of range"}

@app.delete("/todo/{item_index}")
def delete_item(item_index: int):
    try:
        deleted_item = todo_items.pop(item_index)
        return {"status": "ok", "message": f"Deleted item: {deleted_item}"}
    except IndexError:
        return {"status": "error", "message": "Item index out of range"}

@app.get("/hello/")
def welcome():
    return "Hello World!"

@app.post("/hello/")
def welcome():
    return "Hello World!"

@app.get("/person/")
def person():
    return {'name':'Jimit', 'address':'India'}

@app.get("/numbers/")
def print_list():
    return list(range(5))

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