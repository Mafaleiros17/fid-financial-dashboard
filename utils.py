import json
import os

DATA_PATH = "data/data.json"

def load_data():
    if not os.path.exists(DATA_PATH):
        return {"lancamentos": []}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")