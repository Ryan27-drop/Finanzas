# 💰 Budget Planner

App web para distribuir tu salario mensual con la regla 30/20/15/15/20, registrar tus ingresos y gastos reales, y llevar historial mes a mes — con modo claro/oscuro.

| Categoría     | Porcentaje |
|---------------|-----------|
| 🏠 Casa        | 30%       |
| 🛒 Básico      | 20%       |
| 💰 Ahorros     | 15%       |
| 🎯 Metas       | 15%       |
| 🎉 Disfrutar   | 20%       |

## Funcionalidades

- **Presupuesto:** ingresa tu salario y mira la distribución animada por categoría.
- **Balance:** registra ingresos y gastos reales del mes, compara gasto real vs. presupuestado por categoría, y mira el balance neto.
- **Historial:** revisa todos los meses guardados, totales anuales, y elimina registros.
- **Modo claro/oscuro:** toggle 🌙 arriba a la derecha.
- **Persistencia real (Supabase):** los datos no se pierden al reiniciar/redeployar la app.

---

## Instalación local

```bash
git clone https://github.com/tu-usuario/budget-planner.git
cd budget-planner
pip install -r requirements.txt
streamlit run app.py
```

La app abre en `http://localhost:8501`.

Sin configuración adicional, la app guarda los datos en archivos JSON locales (`budget_data.json`, `transactions.json`) — funciona perfecto para probar, pero esos archivos **no persisten** si haces redeploy en Streamlit Cloud.

---

## Persistencia permanente con Supabase (recomendado)

Streamlit Cloud reinicia el sistema de archivos en cada redeploy. Para que tus datos **nunca se pierdan**, conecta una base de datos gratuita de Supabase:

### 1. Crea un proyecto en Supabase

1. Ve a [supabase.com](https://supabase.com) → **New project** (plan gratuito).
2. Cuando esté listo, ve a **SQL Editor** y ejecuta:

```sql
create table budget_records (
  id bigint generated always as identity primary key,
  year int not null,
  month int not null,
  salary numeric not null,
  distribution jsonb not null,
  saved_at text,
  unique (year, month)
);

create table transactions (
  id bigint generated always as identity primary key,
  year int not null,
  month int not null,
  type text not null,        -- 'ingreso' o 'gasto'
  category text,
  description text,
  amount numeric not null,
  date date not null
);
```

3. Ve a **Project Settings → API** y copia:
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_KEY`

### 2. Configura las credenciales

**Local:** copia `.streamlit/secrets.toml.example` a `.streamlit/secrets.toml` y rellena los valores. Este archivo está en `.gitignore`, nunca se sube a GitHub.

**Streamlit Cloud:** en tu app desplegada → **Settings → Secrets** → pega:

```toml
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-anon-key-publica"
```

Guarda y la app se reinicia automáticamente. A partir de ahí, todos los presupuestos y movimientos se guardan en Supabase y persisten para siempre, sin importar cuántas veces redeployes.

> Si no configuras Supabase, la app sigue funcionando con almacenamiento local JSON (verás un aviso ℹ️ en la parte superior).

---

## Deploy en Streamlit Cloud

1. Sube el repo a GitHub (incluye `app.py`, `db.py`, `requirements.txt`).
2. Ve a [share.streamlit.io](https://share.streamlit.io) → **New app** → selecciona tu repo → Main file: `app.py` → **Deploy**.
3. (Opcional pero recomendado) Configura los secrets de Supabase como se explicó arriba.

---

## Estructura del proyecto

```
budget-planner/
├── app.py                          # Interfaz y lógica principal
├── db.py                           # Capa de persistencia (Supabase + fallback JSON)
├── requirements.txt                # Dependencias
├── .streamlit/
│   └── secrets.toml.example        # Plantilla de credenciales Supabase
├── budget_data.json                # (local, generado, no se sube a git)
├── transactions.json               # (local, generado, no se sube a git)
└── README.md
```

---

## Tecnologías

- [Streamlit](https://streamlit.io) — UI web en Python
- [Pandas](https://pandas.pydata.org) — manejo de tablas
- [Supabase](https://supabase.com) — base de datos Postgres gratuita para persistencia
