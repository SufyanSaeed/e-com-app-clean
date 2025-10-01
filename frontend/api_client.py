import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

TIMEOUT = 10

def _headers(token=None):
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers



def register(username, email, password):
    payload = {"username": username, "email": email, "password": password}
    r = requests.post(f"{API_URL}/register", json=payload, timeout=TIMEOUT)
    return r

def login(username, password):
    payload = {"username": username, "password": password}
    r = requests.post(f"{API_URL}/login", json=payload, timeout=TIMEOUT)
    # expected to return {"access_token": "...", "token_type": "bearer"} or similar
    return r

def get_products(token=None):
    try:
        r = requests.get(f"{API_URL}/ecomProducts", timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json()
        else:
            return []  # ya None, taake app crash na kare
    except Exception as e:
        print("Error fetching products:", e)
        return []
    

def is_admin(username):
    try:
        r = requests.get(f"{API_URL}/is_admin/{username}", timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json().get("is_admin", False)
        return False
    except:
        return False
    
def add_product(payload, token):
    return requests.post(f"{API_URL}/addProducts", json=payload, headers=_headers(token), timeout=TIMEOUT)

def delete_product(prod_id, token):
    return requests.delete(f"{API_URL}/ecomProducts/{prod_id}", headers=_headers(token), timeout=TIMEOUT)


def update_product(prod_id, payload, token):
    return requests.put(f"{API_URL}/ecomProducts/{prod_id}", json=payload, headers=_headers(token), timeout=TIMEOUT)

def add_to_cart(payload,token):
    return requests.post(f"{API_URL}/cartAdd",json=payload,headers=_headers(token), timeout=TIMEOUT)

def view_cart(token):
    return requests.get(f"{API_URL}/viewCart",headers=_headers(token), timeout=TIMEOUT)

def checkout(token):
    return requests.get(f"{API_URL}/checkout",headers=_headers(token), timeout=TIMEOUT)

def myOrders(token):
    return requests.get(f"{API_URL}/order",headers=_headers(token), timeout=TIMEOUT)





    
