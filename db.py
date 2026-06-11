"""
Capa de persistencia.

- Si existen las claves SUPABASE_URL y SUPABASE_KEY en st.secrets, todo se
  guarda en Supabase (Postgres) -> persistencia real, sobrevive reinicios
  y redeploys de Streamlit Cloud.
- Si no existen, se usa un fallback local en archivos JSON (útil para
  probar la app en tu máquina sin configurar nada).
"""

import json
import os
import streamlit as st

BUDGET_FILE = "budget_data.json"
TRANSACTIONS_FILE = "transactions.json"


# ─────────────────────────────────────────────────────────────────────────
# CLIENTE SUPABASE
# ─────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        from supabase import create_client
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    return None


def using_supabase():
    return get_client() is not None


# ─────────────────────────────────────────────────────────────────────────
# HELPERS LOCALES (JSON)
# ─────────────────────────────────────────────────────────────────────────
def _load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────
# REGISTROS DE PRESUPUESTO (budget_records)
# ─────────────────────────────────────────────────────────────────────────
def load_budget_records():
    """Devuelve un dict { 'YYYY-MM': {year, month, salary, distribution, saved_at} }"""
    client = get_client()
    if client:
        res = client.table("budget_records").select("*").execute()
        out = {}
        for row in res.data:
            key = f"{row['year']}-{row['month']:02d}"
            out[key] = {
                "year": row["year"],
                "month": row["month"],
                "salary": row["salary"],
                "distribution": row["distribution"],
                "saved_at": row.get("saved_at", ""),
            }
        return out
    return _load_json(BUDGET_FILE)


def save_budget_record(year, month, salary, distribution):
    client = get_client()
    from datetime import datetime
    saved_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    if client:
        existing = (
            client.table("budget_records")
            .select("id")
            .eq("year", year)
            .eq("month", month)
            .execute()
        )
        payload = {
            "year": year,
            "month": month,
            "salary": salary,
            "distribution": distribution,
            "saved_at": saved_at,
        }
        if existing.data:
            client.table("budget_records").update(payload).eq(
                "id", existing.data[0]["id"]
            ).execute()
        else:
            client.table("budget_records").insert(payload).execute()
        return

    data = _load_json(BUDGET_FILE)
    key = f"{year}-{month:02d}"
    data[key] = {
        "year": year,
        "month": month,
        "salary": salary,
        "distribution": distribution,
        "saved_at": saved_at,
    }
    _save_json(BUDGET_FILE, data)


def delete_budget_record(year, month):
    client = get_client()
    if client:
        client.table("budget_records").delete().eq("year", year).eq(
            "month", month
        ).execute()
        return

    data = _load_json(BUDGET_FILE)
    key = f"{year}-{month:02d}"
    if key in data:
        del data[key]
        _save_json(BUDGET_FILE, data)


# ─────────────────────────────────────────────────────────────────────────
# TRANSACCIONES (transactions) -> ingresos y gastos
# ─────────────────────────────────────────────────────────────────────────
def load_transactions(year, month):
    """Devuelve lista de transacciones del mes, ordenadas por fecha."""
    client = get_client()
    if client:
        res = (
            client.table("transactions")
            .select("*")
            .eq("year", year)
            .eq("month", month)
            .order("date")
            .execute()
        )
        return res.data

    data = _load_json(TRANSACTIONS_FILE)
    items = [t for t in data.values() if t["year"] == year and t["month"] == month]
    return sorted(items, key=lambda t: t["date"])


def load_all_transactions():
    client = get_client()
    if client:
        res = client.table("transactions").select("*").order("date").execute()
        return res.data

    data = _load_json(TRANSACTIONS_FILE)
    return sorted(data.values(), key=lambda t: t["date"])


def add_transaction(year, month, ttype, category, description, amount, date):
    client = get_client()
    payload = {
        "year": year,
        "month": month,
        "type": ttype,
        "category": category,
        "description": description,
        "amount": amount,
        "date": date,
    }
    if client:
        client.table("transactions").insert(payload).execute()
        return

    data = _load_json(TRANSACTIONS_FILE)
    new_id = str(max([int(k) for k in data.keys()], default=0) + 1)
    payload["id"] = new_id
    data[new_id] = payload
    _save_json(TRANSACTIONS_FILE, data)


def delete_transaction(transaction_id):
    client = get_client()
    if client:
        client.table("transactions").delete().eq("id", transaction_id).execute()
        return

    data = _load_json(TRANSACTIONS_FILE)
    key = str(transaction_id)
    if key in data:
        del data[key]
        _save_json(TRANSACTIONS_FILE, data)
