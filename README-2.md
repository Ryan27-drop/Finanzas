# 💰 Finanzas Utah

App web estática (HTML + CSS + JS puro) para distribuir tu salario mensual con la regla 30/20/15/15/20, registrar ingresos y gastos reales, y llevar historial mes a mes — con modo claro/oscuro.

| Categoría     | Porcentaje |
|---------------|-----------|
| 🏠 Casa        | 30%       |
| 🛒 Básico      | 20%       |
| 💰 Ahorros     | 15%       |
| 🎯 Metas       | 15%       |
| 🎉 Disfrutar   | 20%       |

## Cómo guarda los datos

Esta versión **no usa ningún backend ni base de datos**. Todo se guarda en el `localStorage` del navegador del dispositivo donde la uses. Eso significa:

- Los datos **persisten** aunque cierres la pestaña, el navegador, o apagues la computadora — no se borran al recargar.
- Los datos **no se sincronizan** entre dispositivos ni navegadores distintos (si abres la app en el celular, verás un historial vacío, separado del de tu computadora).
- Si borras los datos de navegación/caché del sitio, o usas modo incógnito, los registros se pierden.

## Funcionalidades

- **Presupuesto:** ingresa tu salario en dólares y mira la distribución animada por categoría.
- **Balance:** registra ingresos y gastos reales del mes, compara gasto real vs. presupuestado por categoría, mira el balance neto.
- **Historial:** revisa todos los meses guardados, totales anuales, y elimina registros.
- **Modo claro/oscuro:** toggle 🌙 en la esquina superior derecha del encabezado, se recuerda entre visitas.

---

## Probar localmente

No necesita instalación ni dependencias. Simplemente abre `index.html` en tu navegador (doble clic, o arrástralo a una pestaña).

Si prefieres servirlo con un mini servidor local (recomendado para evitar restricciones del navegador con archivos locales):

```bash
# Con Python instalado:
python3 -m http.server 8000
# Abre http://localhost:8000
```

---

## Deploy en Vercel

### Opción A — Desde GitHub (recomendado)

1. Sube este proyecto a un repositorio en GitHub (debe incluir `index.html` y `vercel.json`).
2. Ve a [vercel.com](https://vercel.com) → **Add New → Project**.
3. Importa tu repositorio de GitHub.
4. Vercel detecta automáticamente que es un sitio estático. No necesitas configurar build command ni output directory.
5. Clic en **Deploy**. En menos de un minuto tienes tu URL pública (`tu-proyecto.vercel.app`).

### Opción B — Desde la CLI de Vercel

```bash
npm install -g vercel
cd finanzas-utah
vercel
```

Sigue las instrucciones en pantalla (login, nombre del proyecto, etc.). Para producción:

```bash
vercel --prod
```

---

## Estructura del proyecto

```
finanzas-utah/
├── index.html       # Toda la app: HTML + CSS + JS en un solo archivo
├── vercel.json       # Configuración de deploy para Vercel
├── .gitignore
└── README.md
```

---

## Tecnologías

- HTML, CSS y JavaScript puro (sin frameworks, sin build step)
- `localStorage` del navegador para persistencia
- [Vercel](https://vercel.com) para hosting estático
