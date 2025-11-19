# 🐾 Veterinaria a Domicilio - Web App (Flask)

Aplicación web desarrollada en **Python + Flask** para gestionar citas
veterinarias a domicilio en León y alrededores.\
Incluye sistema de reservas, validaciones, formularios WTForms, gestión
de disponibilidad y páginas informativas.

## 🚀 Tecnologías utilizadas

-   Python 3.10+
-   Flask
-   WTForms
-   Bootstrap 5
-   Jinja2
-   SQLite / MySQL
-   Email Validator

## 📂 Estructura del proyecto

    ├── app.py
    ├── /booking
    │   ├── forms.py
    │   ├── routes.py
    │   ├── utils.py
    ├── /templates
    │   ├── base.html
    │   ├── booking/
    │   │   ├── nueva_cita.html
    │   │   ├── confirmacion.html
    │   ├── cobertura.html
    ├── /static
    │   ├── css/
    │   ├── js/
    │   ├── img/
    ├── requirements.txt
    └── README.md

## ⚙️ Instalación

1.  Clonar el repositorio:

```{=html}
<!-- -->
```
    git clone https://github.com/tuusuario/tu-repo.git
    cd tu-repo

2.  Crear entorno virtual:

```{=html}
<!-- -->
```
    python -m venv env
    source env/bin/activate  # Linux/Mac
    env\Scripts\activate   # Windows

3.  Instalar dependencias:

```{=html}
<!-- -->
```
    pip install -r requirements.txt

4.  Ejecutar la aplicación:

```{=html}
<!-- -->
```
    flask run

## 🗓️ Funcionalidades principales

✔️ Reserva de citas veterinarias\
✔️ Validación con WTForms\
✔️ Gestión de fechas y horarios\
✔️ Página de cobertura (León y alrededores)\
✔️ Email de confirmación (opcional)\
✔️ Bootstrap 5 responsive

## 🌍 Cobertura

-   León capital\
-   San Andrés del Rabanedo\
-   La Virgen del Camino\
-   Trobajo del Camino\
-   Villaobispo / Navatejera\
-   Otras zonas bajo disponibilidad

## 🛠️ Variables de entorno

    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    DATABASE_URL=sqlite:///data.db

## 📦 Paquetes adicionales

    pip install email_validator

## 📄 Licencia

MIT

## ✉️ Contacto

📧 tuemail@ejemplo.com
