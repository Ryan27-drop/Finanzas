import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mi Presupuesto",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ─────────────────────────────────────────────────────────────────
DATA_FILE = "budget_data.json"

CATEGORIES = {
    "🏠 Casa":        {"pct": 0.30, "color": "#1A56DB"},
    "🛒 Básicos":     {"pct": 0.20, "color": "#2563EB"},
    "💰 Ahorros":     {"pct": 0.15, "color": "#3B82F6"},
    "🎯 Metas":       {"pct": 0.15, "color": "#60A5FA"},
    "🎉 Disfrutar":   {"pct": 0.20, "color": "#93C5FD"},
}

MONTHS = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

CURRENT_YEAR = datetime.now().year

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #F8FAFF;
    }

    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #1A56DB 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        margin: 0.4rem 0 0 0;
        opacity: 0.8;
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* Salary card */
    .salary-display {
        background: white;
        border: 2px solid #EBF2FF;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .salary-display .label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6B7280;
        margin-bottom: 0.4rem;
    }
    .salary-display .amount {
        font-size: 2.4rem;
        font-weight: 700;
        color: #1E3A5F;
        letter-spacing: -1px;
    }

    /* Category cards */
    .cat-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid;
        margin-bottom: 0.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .cat-name {
        font-weight: 600;
        font-size: 0.95rem;
        color: #1E3A5F;
    }
    .cat-pct {
        font-size: 0.78rem;
        color: #6B7280;
        margin-top: 2px;
    }
    .cat-amount {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1A56DB;
    }

    /* Progress bar section */
    .progress-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .section-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6B7280;
        margin-bottom: 1rem;
    }

    /* Table styling */
    .history-table {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #1E3A5F !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label {
        color: rgba(255,255,255,0.85) !important;
        font-weight: 500;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1A56DB;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #1E3A5F;
        color: white;
    }

    /* Success / warning banners */
    .stSuccess {
        border-radius: 8px;
    }

    /* Hide Streamlit default footer */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Data helpers ──────────────────────────────────────────────────────────────
def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def record_key(year: int, month: str) -> str:
    return f"{year}-{month}"


# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>💰 Mi Presupuesto</h1>
    <p>Distribución inteligente de ingresos por mes</p>
</div>
""", unsafe_allow_html=True)

data = load_data()

# ── Sidebar: input ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📅 Registro mensual")
    st.markdown("---")

    year = st.selectbox("Año", list(range(CURRENT_YEAR - 2, CURRENT_YEAR + 3)), index=2)
    month = st.selectbox("Mes", MONTHS, index=datetime.now().month - 1)
    salary = st.number_input(
        "Salario / Ingresos (₡)",
        min_value=0.0,
        step=10000.0,
        format="%.0f",
        placeholder="Ej: 800000",
    )

    st.markdown("---")
    if st.button("💾 Guardar registro"):
        if salary > 0:
            key = record_key(year, month)
            data[key] = {"year": year, "month": month, "salary": salary}
            save_data(data)
            st.success(f"✅ {month} {year} guardado")
        else:
            st.warning("Ingresa un monto mayor a 0")

    st.markdown("---")
    st.markdown("### 🗑️ Eliminar registro")
    existing_keys = sorted(data.keys(), reverse=True)
    if existing_keys:
        del_key = st.selectbox("Registro a eliminar", existing_keys)
        if st.button("Eliminar"):
            data.pop(del_key, None)
            save_data(data)
            st.success(f"Eliminado: {del_key}")
    else:
        st.caption("Sin registros aún")


# ── Main: current calculation ─────────────────────────────────────────────────
col_left, col_right = st.columns([1.1, 1.9], gap="large")

with col_left:
    # Salary display
    display_salary = salary if salary > 0 else 0
    st.markdown(f"""
    <div class="salary-display">
        <div class="label">Ingreso seleccionado</div>
        <div class="amount">₡{display_salary:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Distribución</div>', unsafe_allow_html=True)

    for cat_name, meta in CATEGORIES.items():
        amount = display_salary * meta["pct"]
        st.markdown(f"""
        <div class="cat-card" style="border-left-color: {meta['color']}">
            <div>
                <div class="cat-name">{cat_name}</div>
                <div class="cat-pct">{int(meta['pct']*100)}% del ingreso</div>
            </div>
            <div class="cat-amount">₡{amount:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Visualización del presupuesto</div>', unsafe_allow_html=True)

    # Horizontal stacked bar via HTML
    if display_salary > 0:
        bar_html = '<div style="display:flex; border-radius:8px; overflow:hidden; height:40px; margin-bottom:1.2rem;">'
        for cat_name, meta in CATEGORIES.items():
            pct = meta["pct"] * 100
            bar_html += f'<div title="{cat_name}: {pct:.0f}%" style="width:{pct}%; background:{meta["color"]}; display:flex; align-items:center; justify-content:center; color:white; font-size:0.75rem; font-weight:600;">{pct:.0f}%</div>'
        bar_html += "</div>"
        st.markdown(bar_html, unsafe_allow_html=True)

        # Legend
        legend_html = '<div style="display:flex; flex-wrap:wrap; gap:0.8rem; margin-bottom:1rem;">'
        for cat_name, meta in CATEGORIES.items():
            amount = display_salary * meta["pct"]
            legend_html += f'''
            <div style="display:flex; align-items:center; gap:0.4rem;">
                <div style="width:10px; height:10px; border-radius:2px; background:{meta["color"]}; flex-shrink:0;"></div>
                <span style="font-size:0.82rem; color:#374151;">{cat_name} — <strong>₡{amount:,.0f}</strong></span>
            </div>'''
        legend_html += "</div>"
        st.markdown(legend_html, unsafe_allow_html=True)
    else:
        st.info("Ingresa un monto en el panel izquierdo para ver la distribución.", icon="👈")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── History table ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-title" style="margin-top:1rem;">📊 Historial anual</div>', unsafe_allow_html=True)

    year_records = {k: v for k, v in data.items() if v.get("year") == year}

    if year_records:
        rows = []
        for k in sorted(year_records.keys()):
            rec = year_records[k]
            s = rec["salary"]
            row = {"Mes": rec["month"], "Ingreso (₡)": f"{s:,.0f}"}
            for cat_name, meta in CATEGORIES.items():
                row[cat_name] = f"{s * meta['pct']:,.0f}"
            rows.append(row)

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Year summary
        total_income = sum(v["salary"] for v in year_records.values())
        st.markdown(f"""
        <div style="background:#EBF2FF; border-radius:10px; padding:1rem 1.5rem; margin-top:1rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:0.78rem; font-weight:600; text-transform:uppercase; letter-spacing:1px; color:#6B7280;">Total acumulado {year}</div>
                <div style="font-size:1.6rem; font-weight:700; color:#1E3A5F;">₡{total_income:,.0f}</div>
            </div>
            <div style="font-size:0.85rem; color:#1A56DB; font-weight:500;">{len(year_records)} mes(es) registrados</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"Sin registros para {year}. Guarda el primer mes desde el panel lateral.", icon="📅")
