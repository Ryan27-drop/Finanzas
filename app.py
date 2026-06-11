import streamlit as st
import pandas as pd
from datetime import datetime, date

import db

# ── CONFIG ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Budget Planner",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CATEGORIES = {
    "🏠 Casa": 0.30,
    "🛒 Básico": 0.20,
    "💰 Ahorros": 0.15,
    "🎯 Metas": 0.15,
    "🎉 Disfrutar": 0.20,
}
SHORT_LABELS = ["Casa", "Básico", "Ahorros", "Metas", "Disfrutar"]
ICONS = ["🏠", "🛒", "💰", "🎯", "🎉"]

EXPENSE_CATEGORIES = ["🏠 Casa", "🛒 Básico", "💰 Ahorros", "🎯 Metas", "🎉 Disfrutar", "🔸 Otro"]
INCOME_CATEGORIES = ["💼 Salario", "➕ Ingreso extra", "🔸 Otro"]

MONTH_NAMES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


# ── THEME ────────────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

LIGHT = {
    "bg": "#F8FAFF",
    "card": "#ffffff",
    "text": "#1B3A6B",
    "text_soft": "#6B8CB8",
    "border": "#E0EAFF",
    "bar_bg": "#E8F0FE",
    "accent": "#4A90D9",
    "accent_dark": "#1B3A6B",
    "shadow": "rgba(74,144,217,0.07)",
    "success_bg": "linear-gradient(90deg, #E8F5E9, #F1F8FF)",
    "success_border": "#90CAF9",
    "danger": "#E15555",
    "danger_bg": "#FDECEC",
    "positive": "#2E9E5B",
    "positive_bg": "#E8F8EF",
}

DARK = {
    "bg": "#0E1726",
    "card": "#16233A",
    "text": "#E8F0FE",
    "text_soft": "#8BADD9",
    "border": "#26395C",
    "bar_bg": "#1F3050",
    "accent": "#5BA0EE",
    "accent_dark": "#5BA0EE",
    "shadow": "rgba(0,0,0,0.35)",
    "success_bg": "linear-gradient(90deg, #16332A, #16233A)",
    "success_border": "#2E5C8A",
    "danger": "#FF6B6B",
    "danger_bg": "#3A1F22",
    "positive": "#5DD89B",
    "positive_bg": "#16332A",
}

T = DARK if st.session_state.dark_mode else LIGHT

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: {T["bg"]};
}}

#MainMenu, footer, header {{visibility: hidden;}}

/* ── HERO ── */
.hero {{
    background: linear-gradient(135deg, #1B3A6B 0%, #2D5AA0 60%, #4A90D9 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(27,58,107,0.18);
}}
.hero h1 {{
    color: #ffffff;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.5px;
}}
.hero p {{
    color: rgba(255,255,255,0.75);
    font-size: 0.95rem;
    margin: 0;
}}

/* ── INPUT CARD ── */
.input-card {{
    background: {T["card"]};
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    border: 1px solid {T["border"]};
    box-shadow: 0 2px 12px {T["shadow"]};
}}

/* ── CATEGORY BARS ── */
.cat-row {{
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    gap: 0.75rem;
}}
.cat-label {{
    width: 130px;
    font-size: 0.88rem;
    font-weight: 500;
    color: {T["text"]};
    flex-shrink: 0;
}}
.cat-bar-bg {{
    flex: 1;
    background: {T["bar_bg"]};
    border-radius: 8px;
    height: 10px;
    overflow: hidden;
}}
.cat-bar-fill {{
    height: 100%;
    border-radius: 8px;
    background: linear-gradient(90deg, #1B3A6B, {T["accent"]});
    transition: width 0.6s cubic-bezier(0.34,1.56,0.64,1);
}}
.cat-amount {{
    width: 110px;
    text-align: right;
    font-size: 0.88rem;
    font-weight: 600;
    color: {T["accent_dark"]};
    flex-shrink: 0;
}}
.cat-pct {{
    width: 38px;
    text-align: right;
    font-size: 0.8rem;
    color: {T["text_soft"]};
    flex-shrink: 0;
}}

/* ── CARDS GRID ── */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}}
.budget-card {{
    background: {T["card"]};
    border: 1px solid {T["border"]};
    border-radius: 14px;
    padding: 1.25rem 1rem;
    text-align: center;
    box-shadow: 0 2px 8px {T["shadow"]};
}}
.budget-card .icon {{ font-size: 1.5rem; }}
.budget-card .label {{
    font-size: 0.78rem;
    color: {T["text_soft"]};
    font-weight: 500;
    margin: 0.3rem 0 0.1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.budget-card .value {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {T["text"]};
}}
.budget-card .pct {{
    font-size: 0.78rem;
    color: {T["accent"]};
    font-weight: 500;
}}

/* ── SUMMARY CARDS (balance) ── */
.summary-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}}
.summary-card {{
    border-radius: 14px;
    padding: 1.25rem 1rem;
    text-align: center;
    border: 1px solid {T["border"]};
}}
.summary-card.income {{ background: {T["positive_bg"]}; }}
.summary-card.expense {{ background: {T["danger_bg"]}; }}
.summary-card.balance {{ background: {T["card"]}; box-shadow: 0 2px 8px {T["shadow"]}; }}
.summary-card .label {{
    font-size: 0.78rem;
    color: {T["text_soft"]};
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.3rem;
}}
.summary-card .value {{ font-size: 1.3rem; font-weight: 700; }}
.summary-card.income .value {{ color: {T["positive"]}; }}
.summary-card.expense .value {{ color: {T["danger"]}; }}
.summary-card.balance .value {{ color: {T["text"]}; }}

/* ── SECTION HEADER ── */
.section-header {{
    color: {T["text"]};
    font-size: 1.1rem;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid {T["border"]};
}}

/* ── SUCCESS BANNER ── */
.success-banner {{
    background: {T["success_bg"]};
    border: 1px solid {T["success_border"]};
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: {T["text"]};
    font-size: 0.9rem;
    margin-bottom: 1rem;
}}

/* ── TABLE ── */
.stDataFrame {{ border-radius: 12px; overflow: hidden; }}

/* Inputs */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stDateInput"] input {{
    border: 1.5px solid {T["border"]};
    border-radius: 10px;
    background: {T["bg"]};
    color: {T["text"]};
    font-weight: 600;
}}
div[data-testid="stSelectbox"] > div {{
    border: 1.5px solid {T["border"]};
    border-radius: 10px;
    background: {T["bg"]};
}}

/* Buttons */
.stButton > button {{
    background: linear-gradient(135deg, #1B3A6B, #2D5AA0);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    transition: opacity 0.2s;
    width: 100%;
}}
.stButton > button:hover {{
    opacity: 0.88;
    border: none;
}}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {{
    background: {T["bar_bg"]};
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 9px;
    color: {T["accent_dark"]};
    font-weight: 500;
    font-size: 0.9rem;
}}
.stTabs [aria-selected="true"] {{
    background: #1B3A6B !important;
    color: white !important;
}}

/* Generic text color fix in dark mode */
.stMarkdown, .stMarkdown p, label, .stCaption {{
    color: {T["text"]};
}}
</style>
""", unsafe_allow_html=True)


# ── HEADER (hero + theme toggle) ─────────────────────────────────────────────
col_hero, col_toggle = st.columns([6, 1])
with col_hero:
    st.markdown("""
    <div class="hero">
        <h1>💰 Budget Planner</h1>
        <p>Distribuye tu salario, registra tus gastos y lleva tu historial</p>
    </div>
    """, unsafe_allow_html=True)
with col_toggle:
    st.write("")
    st.write("")
    st.toggle("🌙", key="dark_mode", help="Modo oscuro")

if not db.using_supabase():
    st.caption("ℹ️ Usando almacenamiento local (JSON). Configura Supabase para persistencia permanente en Streamlit Cloud — ver README.")

current_year = datetime.now().year
current_month = datetime.now().month

tab1, tab2, tab3 = st.tabs(["📊 Presupuesto", "📈 Balance", "📅 Historial"])

# ═══════════════════════════════════════════════════════════
# TAB 1 — PRESUPUESTO
# ═══════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        salary = st.number_input(
            "💵 Ingreso del mes (₡ o $)",
            min_value=0.0,
            step=10000.0,
            format="%.2f",
            placeholder="Ej: 850000",
        )
    with col2:
        year_p = st.selectbox("Año", list(range(current_year - 1, current_year + 3)), index=1, key="y_presup")
    with col3:
        month_p = st.selectbox(
            "Mes",
            list(range(1, 13)),
            format_func=lambda x: MONTH_NAMES[x],
            index=current_month - 1,
            key="m_presup",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if salary > 0:
        distribution = {cat: salary * pct for cat, pct in CATEGORIES.items()}

        st.markdown('<p class="section-header">Distribución</p>', unsafe_allow_html=True)

        bars_html = ""
        for cat, amount in distribution.items():
            pct = CATEGORIES[cat]
            bars_html += f"""
            <div class="cat-row">
                <div class="cat-label">{cat}</div>
                <div class="cat-bar-bg">
                    <div class="cat-bar-fill" style="width:{pct*100}%;"></div>
                </div>
                <div class="cat-amount">{amount:,.0f}</div>
                <div class="cat-pct">{pct*100:.0f}%</div>
            </div>
            """
        st.markdown(bars_html, unsafe_allow_html=True)

        cards_html = '<div class="cards-grid">'
        for i, (cat, amount) in enumerate(distribution.items()):
            pct = CATEGORIES[cat]
            cards_html += f"""
            <div class="budget-card">
                <div class="icon">{ICONS[i]}</div>
                <div class="label">{SHORT_LABELS[i]}</div>
                <div class="value">{amount:,.0f}</div>
                <div class="pct">{pct*100:.0f}%</div>
            </div>
            """
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

        records = db.load_budget_records()
        key_p = f"{year_p}-{month_p:02d}"
        if key_p in records:
            st.markdown(
                f'<div class="success-banner">✅ Ya hay un registro para <b>{MONTH_NAMES[month_p]} {year_p}</b>. Guardar lo sobreescribirá.</div>',
                unsafe_allow_html=True,
            )

        if st.button(f"💾 Guardar {MONTH_NAMES[month_p]} {year_p}"):
            db.save_budget_record(
                year_p, month_p, salary,
                {cat: round(amt, 2) for cat, amt in distribution.items()},
            )
            st.success(f"✅ Registro guardado para {MONTH_NAMES[month_p]} {year_p}")
            st.rerun()
    else:
        st.info("👆 Ingresa tu salario o ingresos del mes para ver la distribución.")


# ═══════════════════════════════════════════════════════════
# TAB 2 — BALANCE (ingresos y gastos reales)
# ═══════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        year_b = st.selectbox("Año", list(range(current_year - 1, current_year + 3)), index=1, key="y_balance")
    with col2:
        month_b = st.selectbox(
            "Mes", list(range(1, 13)),
            format_func=lambda x: MONTH_NAMES[x],
            index=current_month - 1,
            key="m_balance",
        )

    # ── Formulario para agregar movimiento ──
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown(f"**Agregar movimiento — {MONTH_NAMES[month_b]} {year_b}**")

    f1, f2 = st.columns(2)
    with f1:
        ttype = st.radio("Tipo", ["Gasto", "Ingreso"], horizontal=True, key="ttype")
    with f2:
        tdate = st.date_input("Fecha", value=date(year_b, month_b, min(datetime.now().day, 28)), key="tdate")

    cat_options = EXPENSE_CATEGORIES if ttype == "Gasto" else INCOME_CATEGORIES
    f3, f4, f5 = st.columns([1.2, 2, 1])
    with f3:
        category = st.selectbox("Categoría", cat_options, key="tcat")
    with f4:
        description = st.text_input("Descripción", placeholder="Ej: Supermercado, salario, etc.", key="tdesc")
    with f5:
        amount_t = st.number_input("Monto", min_value=0.0, step=1000.0, format="%.2f", key="tamount")

    if st.button("➕ Agregar movimiento"):
        if amount_t > 0:
            db.add_transaction(
                year_b, month_b,
                "ingreso" if ttype == "Ingreso" else "gasto",
                category, description, amount_t, tdate.isoformat(),
            )
            st.success("Movimiento agregado")
            st.rerun()
        else:
            st.warning("Ingresa un monto mayor a 0.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Resumen del mes ──
    transactions = db.load_transactions(year_b, month_b)
    total_income = sum(t["amount"] for t in transactions if t["type"] == "ingreso")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "gasto")
    net_balance = total_income - total_expense

    st.markdown('<p class="section-header">Resumen del mes</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-grid">
        <div class="summary-card income">
            <div class="label">Ingresos</div>
            <div class="value">{total_income:,.0f}</div>
        </div>
        <div class="summary-card expense">
            <div class="label">Gastos</div>
            <div class="value">{total_expense:,.0f}</div>
        </div>
        <div class="summary-card balance">
            <div class="label">Balance neto</div>
            <div class="value">{net_balance:,.0f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Gastado vs presupuestado por categoría ──
    records = db.load_budget_records()
    key_b = f"{year_b}-{month_b:02d}"
    if key_b in records:
        st.markdown('<p class="section-header">Gastado vs. presupuestado</p>', unsafe_allow_html=True)
        plan = records[key_b]["distribution"]
        bars_html = ""
        for cat in CATEGORIES.keys():
            planned = plan.get(cat, 0)
            spent = sum(t["amount"] for t in transactions if t["type"] == "gasto" and t["category"] == cat)
            pct = min(spent / planned, 1.0) if planned > 0 else 0
            over = spent > planned
            bar_color = T["danger"] if over else f'linear-gradient(90deg, #1B3A6B, {T["accent"]})'
            bars_html += f"""
            <div class="cat-row">
                <div class="cat-label">{cat}</div>
                <div class="cat-bar-bg">
                    <div class="cat-bar-fill" style="width:{pct*100}%; background:{bar_color};"></div>
                </div>
                <div class="cat-amount">{spent:,.0f} / {planned:,.0f}</div>
            </div>
            """
        st.markdown(bars_html, unsafe_allow_html=True)
    else:
        st.info(f"💡 Aún no guardaste un presupuesto para {MONTH_NAMES[month_b]} {year_b} — ve a la pestaña Presupuesto para comparar gastos vs. plan.")

    # ── Lista de movimientos ──
    st.markdown('<p class="section-header">Movimientos del mes</p>', unsafe_allow_html=True)
    if not transactions:
        st.info("No hay movimientos registrados para este mes.")
    else:
        for t in transactions:
            c1, c2, c3, c4, c5 = st.columns([1, 1.5, 2.5, 1.2, 0.8])
            sign = "+" if t["type"] == "ingreso" else "−"
            color = T["positive"] if t["type"] == "ingreso" else T["danger"]
            c1.write(t["date"])
            c2.write(t["category"])
            c3.write(t["description"] or "—")
            c4.markdown(f'<span style="color:{color}; font-weight:600;">{sign} {t["amount"]:,.0f}</span>', unsafe_allow_html=True)
            if c5.button("🗑️", key=f"del_{t['id']}"):
                db.delete_transaction(t["id"])
                st.rerun()


# ═══════════════════════════════════════════════════════════
# TAB 3 — HISTORIAL
# ═══════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-header">Historial por año</p>', unsafe_allow_html=True)

    records = db.load_budget_records()
    all_transactions = db.load_all_transactions()

    years_with_data = set(v["year"] for v in records.values()) | set(t["year"] for t in all_transactions)

    if not years_with_data:
        st.info("Aún no hay registros guardados. Ve a Presupuesto o Balance para empezar.")
    else:
        selected_year = st.selectbox("Filtrar por año", sorted(years_with_data, reverse=True))

        # Resumen de presupuesto guardado
        year_records = {k: v for k, v in records.items() if v["year"] == selected_year}
        if year_records:
            rows = []
            for key in sorted(year_records.keys()):
                rec = year_records[key]
                dist = rec["distribution"]
                rows.append({
                    "Mes": MONTH_NAMES[rec["month"]],
                    "Ingreso": f"{rec['salary']:,.0f}",
                    "🏠 Casa": f"{dist.get('🏠 Casa', 0):,.0f}",
                    "🛒 Básico": f"{dist.get('🛒 Básico', 0):,.0f}",
                    "💰 Ahorros": f"{dist.get('💰 Ahorros', 0):,.0f}",
                    "🎯 Metas": f"{dist.get('🎯 Metas', 0):,.0f}",
                    "🎉 Disfrutar": f"{dist.get('🎉 Disfrutar', 0):,.0f}",
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            total_income_year = sum(v["salary"] for v in year_records.values())
            st.markdown(
                f'<div class="success-banner">📊 Total de ingresos planificados en <b>{selected_year}</b>: <b>{total_income_year:,.0f}</b> — en <b>{len(year_records)}</b> mes(es)</div>',
                unsafe_allow_html=True,
            )
        else:
            st.info(f"No hay presupuestos guardados para {selected_year}.")

        # Resumen de balance real por mes
        st.markdown('<p class="section-header">Balance real por mes</p>', unsafe_allow_html=True)
        year_transactions = [t for t in all_transactions if t["year"] == selected_year]
        if year_transactions:
            balance_rows = []
            for m in range(1, 13):
                month_t = [t for t in year_transactions if t["month"] == m]
                if not month_t:
                    continue
                inc = sum(t["amount"] for t in month_t if t["type"] == "ingreso")
                exp = sum(t["amount"] for t in month_t if t["type"] == "gasto")
                balance_rows.append({
                    "Mes": MONTH_NAMES[m],
                    "Ingresos": f"{inc:,.0f}",
                    "Gastos": f"{exp:,.0f}",
                    "Balance": f"{inc - exp:,.0f}",
                })
            st.dataframe(pd.DataFrame(balance_rows), use_container_width=True, hide_index=True)
        else:
            st.info(f"No hay movimientos de balance registrados para {selected_year}.")

        # Eliminar presupuesto
        if year_records:
            st.markdown('<p class="section-header">Eliminar presupuesto guardado</p>', unsafe_allow_html=True)
            months_available = {MONTH_NAMES[v["month"]]: (v["year"], v["month"]) for v in year_records.values()}
            month_to_delete = st.selectbox("Seleccionar mes a eliminar", list(months_available.keys()))

            if st.button(f"🗑️ Eliminar presupuesto de {month_to_delete} {selected_year}"):
                y, m = months_available[month_to_delete]
                db.delete_budget_record(y, m)
                st.success(f"Presupuesto de {month_to_delete} {selected_year} eliminado.")
                st.rerun()
