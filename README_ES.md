
# 📚 RobaMangas Supremo 🥷 — El Asesino de Loading Gears

¡Bienvenido a RobaMangas Supremo!  
Una herramienta creada con precisión ninja 🥷 para **descargar automáticamente mangas desde InManga.com**, con imágenes en **alta calidad**, **ordenadas por capítulos** y convertidas a **JPG** al vuelo.

---

## 🚀 ¿Qué hace?

- ✅ Extrae todos los capítulos de un manga automáticamente.
- ✅ Realiza scroll infinito para cargar todos los capítulos.
- ✅ Detecta y descarga **todas las imágenes del capítulo**, evitando los molestos *"loading gears"*.
- ✅ Convierte las imágenes a JPG con modo RGB (ideal para lectores o colecciones).
- ✅ Organiza los capítulos en carpetas numeradas limpias (`1`, `2`, `3`...).
- ✅ Modo *headless* con Selenium para que corra todo en segundo plano.
- ✅ Proceso totalmente **automático y escalable**.

---

## 💡 ¿Cómo usarlo?

### 1. Clona o descarga este repositorio

```bash
git clone https://github.com/tuusuario/Roba-Mangas-Supremo.git
cd Roba-Mangas-Supremo
```

O simplemente guarda el archivo `Roba-Mangas-Supremo.py`.

### 2. Instala las dependencias necesarias

```bash
pip install selenium requests pillow
```

También necesitas tener [ChromeDriver](https://chromedriver.chromium.org/) instalado y accesible desde tu PATH.

> 💡 El script usa Selenium con Chrome en modo headless para navegar por las páginas sin abrir una ventana gráfica.

### 3. Ejecuta el script

```bash
python robamangas.py
```

Introduce la URL del manga cuando te la pida. Por ejemplo:

```
https://inmanga.com/ver/manga/Berserk/5cc13fca-2e10-41e7-bbca-d70353d6a55a
```

---

## 🗂 Estructura generada

```
📁 berserk/
 ├── 📁 1/
 │    ├── 1.jpg
 │    ├── 2.jpg
 ├── 📁 2/
 │    ├── 1.jpg
 └── 📁 3/
```

---

## 🧠 Requisitos

- Python 3.7+
- Google Chrome
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

---

## 🔒 Disclaimer

Este script es solo para fines personales y educativos.  
Respeta los derechos de autor y no lo uses para distribución ilegal.

---

## ✨ Créditos

Creado por **@andersanzo** con pasión por el manga y el código limpio.  
¡Dale una estrella ⭐ si te sirvió!

---

> "En la guerra como en el código, la estrategia lo es todo." – Tú, probablemente 😎
