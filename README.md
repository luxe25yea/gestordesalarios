# � Gestor de Salarios - Aguas Moya

<div align="center">

**Aplicación de escritorio para la gestión integral de empleados, jornadas laborales y nóminas**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

[Características](#-características-principales) • [Instalación](#-instalación) • [Uso](#-cómo-usar) • [Estructura](#-estructura-del-proyecto) • [Troubleshooting](#-solución-de-problemas)

</div>

---

## 📋 Descripción

Gestor de Salarios es una aplicación de escritorio desarrollada en **Python** con interfaz gráfica moderna para la gestión completa de empleados, control de asistencia y cálculo automático de nómina. 

Diseñada bajo una arquitectura **MVC (Modelo - Vista - Controlador)** que garantiza un código organizado, escalable y mantenible, perfecto para empresas que necesitan administrar su nómina de forma eficiente.

---

## 🚀 Características principales

- 👤 **Gestión de Empleados** - Crear, editar, eliminar empleados con sus datos de puesto y salario
- 🕒 **Control de Asistencia** - Registrar días trabajados y jornadas laborales por empleado
- 💰 **Cálculo de Nómina** - Generación automática de nóminas basadas en la asistencia
- 📊 **Reportes Dinámicos** - Visualización de reportes con gráficas interactivas
- 📄 **Exportación PDF** - Genera reportes y nóminas en formato PDF
- 🔐 **Sistema de Autenticación** - Control de acceso con usuario y contraseña
- 🎨 **Interfaz Moderna** - Diseño oscuro y profesional con CustomTkinter

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Propósito |
|---|---|
| 🐍 **Python 3.8+** | Lenguaje principal |
| 🗄️ **SQLite3** | Base de datos local |
| 📦 **CustomTkinter** | Interfaz gráfica moderna |
| 📊 **Matplotlib** | Generación de gráficas |
| 📄 **ReportLab** | Creación de PDFs |
| 🔒 **Hashlib** | Encriptación de contraseñas |

---

## 📦 Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- SQLite3 (incluido en Python)

---

## 📥 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/luxe25yea/gestordesalarios.git
cd gestordesalarios
```

### 2️⃣ Crear un entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Iniciar la aplicación

```bash
python main.py
```

---

## 🚀 Cómo usar

### Primer inicio
Al abrir la aplicación por primera vez, se creará automáticamente:
- La base de datos SQLite en `gestordesalarios/data/aguas_moya.db`
- Usuario administrador por defecto

### Credenciales por defecto

```
Usuario: admin
Contraseña: admin123
```

⚠️ **Importante:** Cambia estas credenciales en producción.

### Funcionalidades principales

#### 👥 Gestión de Empleados
- Accede a la sección "Empleados"
- Agrega nuevos empleados con su nombre, puesto y salario diario
- Edita o elimina registros existentes

#### 📅 Control de Jornadas
- Registra los días trabajados por cada empleado
- Visualiza el historial de asistencia
- Calcula automáticamente los totales

#### 💼 Nómina
- Genera nóminas automáticamente basadas en los días trabajados
- Exporta a PDF para distribución
- Visualiza reportes detallados

#### 📊 Reportes
- Gráficas de salarios, asistencia y productividad
- Filtrado por período
- Exportación de datos

---

## 📁 Estructura del proyecto

```
gestordesalarios/
│
├── 📂 controllers/           # Controladores (lógica de interacción)
│   ├── empleado_controller.py
│   ├── login_controller.py
│   └── reporte_controller.py
│
├── 📂 models/                # Modelos de datos
│   ├── usuario.py
│   ├── empleado.py
│   └── asistencia.py
│
├── 📂 views/                 # Vistas (interfaz gráfica)
│   ├── login_view.py
│   ├── dashboard_view.py
│   ├── empleados_view.py
│   ├── jornadas_view.py
│   └── reportes_view.py
│
├── 📂 services/              # Servicios (lógica de negocio)
│   ├── auth_service.py
│   ├── empleado_service.py
│   └── nomina_service.py
│
├── 📂 database/              # Conexión y configuración BD
│   ├── connection.py
│   └── init_db.py
│
├── 📂 utils/                 # Utilidades
│   ├── hash.py               # Encriptación de contraseñas
│   ├── charts.py             # Generación de gráficas
│   └── pdf_generator.py      # Exportación a PDF
│
├── 📂 data/                  # Base de datos (git-ignored)
│   └── aguas_moya.db
│
├── main.py                   # 🚀 Punto de entrada
├── config.py                 # ⚙️ Configuración global
├── requirements.txt          # 📦 Dependencias
└── README.md                 # 📖 Este archivo
```

---

## 🔐 Autenticación

El sistema implementa autenticación segura:
- Contraseñas encriptadas con **SHA-256**
- Validación en cada acceso
- Sesiones de usuario

Para crear nuevos usuarios, contacta al administrador del sistema.

---

## ⚙️ Configuración

Edita `config.py` para personalizar:

```python
# Rutas de base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'aguas_moya.db')
```

---

## 🆘 Solución de problemas

### ❌ "Usuario o contraseña incorrectos"

1. Verifica que escribiste correctamente: `admin` / `admin123`
2. La base de datos podría no estar inicializada. Ejecuta:
   ```bash
   python -c "from database.init_db import initialize_database; initialize_database()"
   ```
3. Si persiste, elimina `data/aguas_moya.db` y reinicia la aplicación

### ❌ "No se encuentra el módulo X"

Instala las dependencias nuevamente:
```bash
pip install -r requirements.txt
```

### ❌ Base de datos no visible

Por defecto, SQLite crea una base de datos invisible. Para ver archivos ocultos:

**Windows (Explorador de archivos):**
- Ver → Mostrar → Elementos ocultos

**Linux/macOS:**
```bash
ls -la gestordesalarios/data/
```

---

## 🚀 Características futuras

- [ ] Exportación a Excel
- [ ] Backups automáticos
- [ ] Integración con APIs de terceros
- [ ] Versión web
- [ ] Sistema de roles y permisos

---

## 📝 Notas de desarrollo

### Arquitectura MVC
- **Models**: Definen la estructura de datos
- **Views**: Interfaz gráfica con CustomTkinter
- **Controllers**: Conectan vistas con servicios
- **Services**: Lógica de negocio

### Base de datos
- SQLite3 para persistencia local
- Esquema normalizado para integridad de datos
- Índices para mejor rendimiento

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**luxe25yea** - Desarrollo y mantenimiento

---

## 📧 Soporte

Si encuentras problemas o tienes sugerencias, abre un [issue](https://github.com/luxe25yea/gestordesalarios/issues) en el repositorio.

---

<div align="center">

**⭐ Si te resultó útil, considera darle una estrella al repositorio ⭐**

</div>

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
