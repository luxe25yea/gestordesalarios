# 💼 Gestor de Salarios

Aplicación de escritorio desarrollada en **Python** para la gestión de empleados, control de asistencia y cálculo de nómina.
Diseñada bajo una arquitectura tipo **MVC (Modelo - Vista - Controlador)** para mantener un código organizado, escalable y mantenible.

---

## 🚀 Características principales

* 👤 Gestión de empleados (altas, bajas, modificaciones)
* 🕒 Control de asistencia y jornadas laborales
* 💰 Cálculo automático de nómina
* 📊 Generación de reportes
* 🔐 Sistema de autenticación de usuarios
* 📄 Exportación de datos (PDF)

---

## 🛠️ Tecnologías utilizadas

* 🐍 Python 3
* 🗄️ SQLite
* 📦 Librerías:

  * `tkinter` (interfaz gráfica)
  * `matplotlib` (gráficas)
  * `reportlab` (generación de PDFs)

---

## 📁 Estructura del proyecto

```
aguas_moya/
│
├── controllers/     # Lógica de control
├── models/          # Modelos de datos
├── views/           # Interfaz gráfica
├── services/        # Lógica de negocio
├── database/        # Conexión y configuración de BD
├── utils/           # Funciones auxiliares
├── data/            # Base de datos (local)
│
├── main.py          # Punto de entrada
├── config.py        # Configuraciones generales
└── requirements.txt # Dependencias
```

---

## ⚙️ Instalación y ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/luxe25yea/gestordesalarios.git
cd gestordesalarios
```

2. Crear entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación:

```bash
python main.py
```

---

## 🔐 Credenciales (ejemplo)

> Puedes modificar esto según tu sistema

* Usuario: `admin`
* Contraseña: `1234`

---

## 📌 Notas

* La base de datos se genera automáticamente si no existe.
* Proyecto orientado a prácticas académicas y aprendizaje.

---

## 👨‍💻 Autor

**Luis Enrique Hernandez Morales**

**Enrique Alexander Bolaños Gutiérrez**

---

## 📄 Licencia

Este proyecto es de uso educativo. Puedes modificarlo y adaptarlo libremente.

---
