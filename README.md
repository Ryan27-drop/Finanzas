# 💰 Mi Presupuesto

Aplicación web para distribuir automáticamente tu salario o ingresos mensuales según reglas de presupuesto personal, con historial por mes y año.

## Distribución de ingresos

| Categoría  | % del ingreso |
|------------|--------------|
| 🏠 Casa     | 30%          |
| 🛒 Básicos  | 20%          |
| 💰 Ahorros  | 15%          |
| 🎯 Metas    | 15%          |
| 🎉 Disfrutar| 20%          |

## Funcionalidades

- Ingresa tu salario para cualquier mes y año
- Distribución automática y visual con barra de porcentajes
- Guarda registros mes a mes en un archivo JSON local
- Historial anual con tabla y total acumulado
- Elimina registros desde el panel lateral

## Instalación local

```bash
git clone https://github.com/TU_USUARIO/mi-presupuesto.git
cd mi-presupuesto
pip install -r requirements.txt
streamlit run app.py
```

## Deploy en Streamlit Cloud

1. Sube el repo a GitHub (incluye `app.py`, `requirements.txt`).
2. Ve a [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Selecciona tu repo, branch `main`, archivo `app.py`.
4. Haz clic en **Deploy**.

> **Nota:** El archivo `budget_data.json` se crea automáticamente al guardar el primer registro. En Streamlit Cloud los datos no persisten entre reinicios del servidor — para persistencia real considera usar [Streamlit secrets + Google Sheets](https://docs.streamlit.io/library/advanced-features/secrets-management) o una base de datos externa.

## Estructura del proyecto

```
mi-presupuesto/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
├── budget_data.json    # Datos guardados (generado automáticamente)
└── README.md
```

## Tecnologías

- [Streamlit](https://streamlit.io/) — interfaz web
- [Pandas](https://pandas.pydata.org/) — manejo de datos tabulares
- JSON — almacenamiento local de registros
