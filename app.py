# app.py
from flask import Flask, render_template_string, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from datetime import datetime
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configuración
ADMIN_PASSWORD = generate_password_hash('jose123')
DATA_FILE = 'data.json'

# Estructura de datos inicial
def init_data():
    return {
        'recursos': [],
        'noticias': [],
        'devocionales': [],
        'lecciones': [],
        'libros': [],
        'videos': [],
        'informacion': {
            'direccion': 'Calle Principal #123, Ciudad',
            'telefono': '+1 (555) 123-4567',
            'email': 'educacion@iglesia.com',
            'horario': 'Lunes a Viernes: 9:00 AM - 5:00 PM'
        },
        'categorias': ['Infantil', 'Adolescentes', 'Jóvenes', 'Adultos', 'Matrimonios', 'Familias']
    }

# Cargar o crear datos
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return init_data()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Templates HTML

BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Departamento de Educación{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --accent-color: #f59e0b;
            --text-color: #1f2937;
            --bg-color: #f3f4f6;
            --white: #ffffff;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.15);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background: var(--bg-color);
        }

        /* Header */
        header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: var(--white);
            padding: 1rem 0;
            box-shadow: var(--shadow-lg);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        .logo h1 {
            font-size: 1.8rem;
            font-weight: 700;
        }

        .logo p {
            font-size: 0.9rem;
            opacity: 0.9;
        }

        nav ul {
            list-style: none;
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
        }

        nav a {
            color: var(--white);
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: background 0.3s;
        }

        nav a:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        /* Container */
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 20px;
        }

        /* Cards */
        .card {
            background: var(--white);
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }

        .card h2 {
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }

        .card h3 {
            color: var(--secondary-color);
            margin: 1rem 0 0.5rem;
            font-size: 1.3rem;
        }

        /* Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        /* Buttons */
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: var(--primary-color);
            color: var(--white);
            text-decoration: none;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s;
            margin: 0.5rem 0.5rem 0.5rem 0;
        }

        .btn:hover {
            background: var(--secondary-color);
        }

        .btn-accent {
            background: var(--accent-color);
        }

        .btn-accent:hover {
            background: #d97706;
        }

        .btn-danger {
            background: #dc2626;
        }

        .btn-danger:hover {
            background: #991b1b;
        }

        /* Forms */
        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--text-color);
        }

        input[type="text"],
        input[type="email"],
        input[type="password"],
        input[type="url"],
        textarea,
        select {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e5e7eb;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        input:focus,
        textarea:focus,
        select:focus {
            outline: none;
            border-color: var(--primary-color);
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        /* Badge */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: var(--primary-color);
            color: var(--white);
            border-radius: 20px;
            font-size: 0.85rem;
            margin: 0.25rem;
        }

        /* Resource Item */
        .resource-item {
            background: var(--white);
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
            box-shadow: var(--shadow);
            margin-bottom: 1rem;
        }

        .resource-item h3 {
            margin-top: 0;
        }

        .resource-meta {
            color: #6b7280;
            font-size: 0.9rem;
            margin: 0.5rem 0;
        }

        /* Info Box */
        .info-box {
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
            margin-bottom: 1rem;
        }

        .info-box h3 {
            color: var(--primary-color);
            margin-top: 0;
        }

        .info-box p {
            margin: 0.5rem 0;
        }

        /* Flash Messages */
        .flash {
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
            animation: slideDown 0.3s ease-out;
        }

        .flash.success {
            background: #d1fae5;
            color: #065f46;
            border-left: 4px solid #10b981;
        }

        .flash.error {
            background: #fee2e2;
            color: #991b1b;
            border-left: 4px solid #ef4444;
        }

        @keyframes slideDown {
            from {
                transform: translateY(-20px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        /* Footer */
        footer {
            background: var(--text-color);
            color: var(--white);
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }

        /* Admin Panel */
        .admin-nav {
            background: var(--white);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            box-shadow: var(--shadow);
        }

        .admin-nav a {
            display: inline-block;
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            background: var(--bg-color);
            color: var(--text-color);
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }

        .admin-nav a:hover,
        .admin-nav a.active {
            background: var(--primary-color);
            color: var(--white);
        }

        /* Table */
        .table-responsive {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--white);
            border-radius: 8px;
            overflow: hidden;
        }

        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }

        th {
            background: var(--primary-color);
            color: var(--white);
            font-weight: 600;
        }

        tr:hover {
            background: var(--bg-color);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                text-align: center;
            }

            nav ul {
                flex-direction: column;
                gap: 0.5rem;
                margin-top: 1rem;
            }

            .grid {
                grid-template-columns: 1fr;
            }

            .logo h1 {
                font-size: 1.5rem;
            }

            .card {
                padding: 1.5rem;
            }

            table {
                font-size: 0.9rem;
            }

            th, td {
                padding: 0.5rem;
            }
        }

        /* Video Container */
        .video-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: 8px;
            margin: 1rem 0;
        }

        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <div class="logo">
                <h1>📚 Departamento de Educación</h1>
                <p>Recursos y Materiales Educativos</p>
            </div>
            <nav>
                <ul>
                    <li><a href="{{ url_for('index') }}">Inicio</a></li>
                    <li><a href="{{ url_for('recursos') }}">Recursos</a></li>
                    <li><a href="{{ url_for('videos') }}">Videos</a></li>
                    <li><a href="{{ url_for('noticias') }}">Noticias</a></li>
                    <li><a href="{{ url_for('devocionales') }}">Devocionales</a></li>
                    <li><a href="{{ url_for('lecciones') }}">Lecciones</a></li>
                    <li><a href="{{ url_for('libros') }}">Libros</a></li>
                    <li><a href="{{ url_for('contacto') }}">Contacto</a></li>
                    {% if session.admin_logged_in %}
                    <li><a href="{{ url_for('admin_dashboard') }}">Admin</a></li>
                    <li><a href="{{ url_for('logout') }}">Salir</a></li>
                    {% endif %}
                </ul>
            </nav>
        </div>
    </header>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <footer>
        <p>&copy; 2024 Departamento de Educación. Todos los derechos reservados.</p>
        <p>Sirviendo a nuestra comunidad con excelencia educativa</p>
    </footer>
</body>
</html>
'''

INDEX_TEMPLATE = '''
{% extends "base.html" %}
{% block content %}
<div class="card">
    <h2>🏠 Bienvenidos</h2>
    <p style="font-size: 1.1rem; line-height: 1.8;">
        Bienvenidos al portal del Departamento de Educación. Aquí encontrarás recursos educativos, 
        materiales de estudio, videos instructivos, devocionales diarios y mucho más para enriquecer 
        tu experiencia de aprendizaje y crecimiento espiritual.
    </p>
</div>

<div class="grid">
    <div class="card">
        <h3>📄 Recursos PDF</h3>
        <p>Accede a materiales descargables para tu estudio personal y grupal.</p>
        <a href="{{ url_for('recursos') }}" class="btn">Ver Recursos</a>
    </div>
    
    <div class="card">
        <h3>🎥 Videos Educativos</h3>
        <p>Contenido multimedia para complementar tu aprendizaje.</p>
        <a href="{{ url_for('videos') }}" class="btn">Ver Videos</a>
    </div>
    
    <div class="card">
        <h3>📰 Noticias</h3>
        <p>Mantente informado sobre las últimas novedades del departamento.</p>
        <a href="{{ url_for('noticias') }}" class="btn">Ver Noticias</a>
    </div>
    
    <div class="card">
        <h3>🙏 Devocionales</h3>
        <p>Reflexiones diarias para tu crecimiento espiritual.</p>
        <a href="{{ url_for('devocionales') }}" class="btn">Ver Devocionales</a>
    </div>
    
    <div class="card">
        <h3>📖 Lecciones de Escuela Sabática</h3>
        <p>Material de estudio semanal para todas las edades.</p>
        <a href="{{ url_for('lecciones') }}" class="btn">Ver Lecciones</a>
    </div>
    
    <div class="card">
        <h3>📚 Biblioteca de Libros</h3>
        <p>Colección de libros digitales para tu edificación.</p>
        <a href="{{ url_for('libros') }}" class="btn">Ver Libros</a>
    </div>
</div>

<div class="card">
    <h2>📍 Últimas Noticias</h2>
    {% if data.noticias[:3] %}
        {% for noticia in data.noticias[:3] %}
        <div class="resource-item">
            <h3>{{ noticia.titulo }}</h3>
            <p class="resource-meta">📅 {{ noticia.fecha }}</p>
            <p>{{ noticia.contenido[:200] }}...</p>
            <a href="{{ url_for('noticias') }}" class="btn">Leer más</a>
        </div>
        {% endfor %}
    {% else %}
        <p>No hay noticias disponibles en este momento.</p>
    {% endif %}
</div>
{% endblock %}
'''

RECURSOS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Recursos PDF - Departamento de Educación{% endblock %}
{% block content %}
<div class="card">
    <h2>📄 Recursos PDF</h2>
    <p>Descarga materiales educativos organizados por categorías.</p>
</div>

{% for categoria in data.categorias %}
    {% set recursos_categoria = data.recursos | selectattr('categoria', 'equalto', categoria) | list %}
    {% if recursos_categoria %}
    <div class="card">
        <h3>📁 {{ categoria }}</h3>
        {% for recurso in recursos_categoria %}
        <div class="resource-item">
            <h3>{{ recurso.titulo }}</h3>
            <span class="badge">{{ recurso.categoria }}</span>
            <p class="resource-meta">📅 {{ recurso.fecha }}</p>
            <p>{{ recurso.descripcion }}</p>
            <a href="{{ recurso.url }}" target="_blank" class="btn">📥 Descargar PDF</a>
        </div>
        {% endfor %}
    </div>
    {% endif %}
{% endfor %}

{% if not data.recursos %}
<div class="card">
    <p>No hay recursos disponibles en este momento.</p>
</div>
{% endif %}
{% endblock %}
'''

VIDEOS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Videos - Departamento de Educación{% endblock %}
{% block content %}
<div class="card">
    <h2>🎥 Videos Educativos</h2>
    <p>Contenido multimedia para tu aprendizaje.</p>
</div>

{% for categoria in data.categorias %}
    {% set videos_categoria = data.videos | selectattr('categoria', 'equalto', categoria) | list %}
    {% if videos_categoria %}
    <div class="card">
        <h3>📺 {{ categoria }}</h3>
        {% for video in videos_categoria %}
        <div class="resource-item">
            <h3>{{ video.titulo }}</h3>
            <span class="badge">{{ video.categoria }}</span>
            <p class="resource-meta">📅 {{ video.fecha }}</p>
            <p>{{ video.descripcion }}</p>
            <div class="video-container">
                <iframe src="{{ video.url }}" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
{% endfor %}

{% if not data.videos %}
<div class="card">
    <p>No hay videos disponibles en este momento.</p>
</div>
{% endif %}
{% endblock %}
'''

NOTICIAS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Noticias - Departamento de Educación{% endblock %}
{% block content %}
<div class="card">
    <h2>📰 Noticias</h2>
    <p>Mantente informado sobre las últimas novedades.</p>
</div>

{% for noticia in data.noticias %}
<div class="card">
    <h3>{{ noticia.titulo }}</h3>
    <p class="resource-meta">📅 {{ noticia.fecha }} | 👤 {{ noticia.autor }}</p>
    <p style="white-space: pre-line;">{{ noticia.contenido }}</p>
</div>
{% endfor %}

{% if not data.noticias %}
<div class="card">
    <p>No hay noticias disponibles en este momento.</p>
</div>
{% endif %}
{% endblock %}
'''

DEVOCIONALES_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Devocionales - Departamento de Educación{% endblock %}
{% block content %}
<div class="card">
    <h2>🙏 Devocionales Diarios</h2>
    <p>Reflexiones para tu crecimiento espiritual.</p>
</div>

{% for devocional in data.devocionales %}
<div class="card">
    <h3>{{ devocional.titulo }}</h3>
    <p class="resource-meta">📅 {{ devocional.fecha }} | 📖 {{ devocional.versiculo }}</p>
    <p style="white-space: pre-line; font-style: italic; background: var(--bg-color); padding: 1rem; border-radius: 5px; margin: 1rem 0;">
        "{{ devocional.texto_biblico }}"
    </p>
    <p style="white-space: pre-line;">{{ devocional.reflexion }}</p>
</div>
{% endfor %}

{% if not data.devocionales %}
<div class="card">
    <p>No hay devocionales disponibles en este momento.</p>
</div>
{% endif %}
{% endblock %}
'''

LECCIONES_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Lecciones - Departamento de Educación{% endblock %}
{% block content %}
<div class="card">
    <h2>📖 Lecciones de Escuela Sabática</h2>
    <p>Material de estudio semanal para todas las edades.</p>
</div>

{% for categoria in data.categorias %}
    {% set lecciones_categoria = data.lecciones | selectattr('categoria', 'equalto', categoria) | list %}
    {% if lecciones_categoria %}
    <div class="card">
        <h3>📚 {{ categoria }}</h3>
        {% for leccion in lecciones_categoria %}
        <div class="resource-item">
            <h3>{{ leccion.titulo }}</h3>
            <span class="badge">{{ leccion.categoria }}</span>
            <p class="resource-meta">📅 {{ leccion.fecha }} | 📆 Trimestre: {{ leccion.trimestre }}</p>
            <p>{{ leccion.descripcion }}</p>
            <a href="{{ leccion.url }}" target="_blank" class="btn">📥 Descargar Lección</a>
        </div>
        {% endfor %}
    </div>
    {% endif %}
{% endfor %}

{% if not data.lecciones %}
<div class="card">
    <p>No hay lecciones disponibles en este momento.</p>
</div>
{% endif %}
{% endblock %}
'''

LIBROS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Libros - Departamento de Educación{% endblock %}
{% block content %}
<div class="card">
    <h2>📚 Biblioteca Digital</h2>
    <p>Colección de libros para tu edificación y estudio.</p>
</div>

{% for categoria in data.categorias %}
    {% set libros_categoria = data.libros | selectattr('categoria', 'equalto', categoria) | list %}
    {% if libros_categoria %}
    <div class="card">
        <h3>📖 {{ categoria }}</h3>
        <div class="grid">
        {% for libro in libros_categoria %}
            <div class="resource-item">
                <h3>{{ libro.titulo }}</h3>
                <span class="badge">{{ libro.categoria }}</span>
                <p class="resource-meta">✍️ {{ libro.autor }}</p>
                <p>{{ libro.descripcion }}</p>
                <a href="{{ libro.url }}" target="_blank" class="btn">📥 Descargar Libro</a>
            </div>
        {% endfor %}
        </div>
    </div>
    {% endif %}
{% endfor %}

{% if not data.libros %}
<div class="card">
    <p>No hay libros disponibles en este momento.</p>
</div>
{% endif %}
{% endblock %}
'''

CONTACTO_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Contacto - Departamento de Educación{% endblock %}
{% block content %}
<div class="card">
    <h2>📍 Información de Contacto</h2>
</div>

<div class="grid">
    <div class="info-box">
        <h3>📍 Dirección</h3>
        <p>{{ data.informacion.direccion }}</p>
    </div>
    
    <div class="info-box">
        <h3>📞 Teléfono</h3>
        <p><a href="tel:{{ data.informacion.telefono }}" style="color: var(--primary-color); text-decoration: none; font-weight: bold;">{{ data.informacion.telefono }}</a></p>
    </div>
    
    <div class="info-box">
        <h3>📧 Email</h3>
        <p><a href="mailto:{{ data.informacion.email }}" style="color: var(--primary-color); text-decoration: none; font-weight: bold;">{{ data.informacion.email }}</a></p>
    </div>
    
    <div class="info-box">
        <h3>🕐 Horario de Atención</h3>
        <p>{{ data.informacion.horario }}</p>
    </div>
</div>

<div class="card">
    <h3>📍 Cómo Llegar</h3>
    <p>Estamos ubicados en {{ data.informacion.direccion }}. Puedes contactarnos por teléfono o email para más información.</p>
    <p style="margin-top: 1rem;">Esperamos tu visita y estamos dispuestos a ayudarte en tu proceso de aprendizaje.</p>
</div>
{% endblock %}
'''

LOGIN_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Login - Admin{% endblock %}
{% block content %}
<div class="card" style="max-width: 400px; margin: 4rem auto;">
    <h2>🔐 Acceso Administrativo</h2>
    <form method="POST">
        <div class="form-group">
            <label for="password">Contraseña:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit" class="btn">Iniciar Sesión</button>
    </form>
</div>
{% endblock %}
'''

ADMIN_DASHBOARD_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Panel de Administración{% endblock %}
{% block content %}
<div class="card">
    <h2>⚙️ Panel de Administración</h2>
    <p>Gestiona todo el contenido del sitio web.</p>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}" {% if section == 'dashboard' %}class="active"{% endif %}>Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}" {% if section == 'recursos' %}class="active"{% endif %}>Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}" {% if section == 'videos' %}class="active"{% endif %}>Videos</a>
    <a href="{{ url_for('admin_noticias') }}" {% if section == 'noticias' %}class="active"{% endif %}>Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}" {% if section == 'devocionales' %}class="active"{% endif %}>Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}" {% if section == 'lecciones' %}class="active"{% endif %}>Lecciones</a>
    <a href="{{ url_for('admin_libros') }}" {% if section == 'libros' %}class="active"{% endif %}>Libros</a>
    <a href="{{ url_for('admin_info') }}" {% if section == 'info' %}class="active"{% endif %}>Información</a>
    <a href="{{ url_for('admin_categorias') }}" {% if section == 'categorias' %}class="active"{% endif %}>Categorías</a>
</div>

<div class="grid">
    <div class="card">
        <h3>📄 Recursos PDF</h3>
        <p style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">{{ data.recursos|length }}</p>
        <a href="{{ url_for('admin_recursos') }}" class="btn">Gestionar</a>
    </div>
    
    <div class="card">
        <h3>🎥 Videos</h3>
        <p style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">{{ data.videos|length }}</p>
        <a href="{{ url_for('admin_videos') }}" class="btn">Gestionar</a>
    </div>
    
    <div class="card">
        <h3>📰 Noticias</h3>
        <p style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">{{ data.noticias|length }}</p>
        <a href="{{ url_for('admin_noticias') }}" class="btn">Gestionar</a>
    </div>
    
    <div class="card">
        <h3>🙏 Devocionales</h3>
        <p style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">{{ data.devocionales|length }}</p>
        <a href="{{ url_for('admin_devocionales') }}" class="btn">Gestionar</a>
    </div>
    
    <div class="card">
        <h3>📖 Lecciones</h3>
        <p style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">{{ data.lecciones|length }}</p>
        <a href="{{ url_for('admin_lecciones') }}" class="btn">Gestionar</a>
    </div>
    
    <div class="card">
        <h3>📚 Libros</h3>
        <p style="font-size: 2rem; font-weight: bold; color: var(--primary-color);">{{ data.libros|length }}</p>
        <a href="{{ url_for('admin_libros') }}" class="btn">Gestionar</a>
    </div>
</div>
{% endblock %}
'''

ADMIN_RECURSOS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Gestionar Recursos - Admin{% endblock %}
{% block content %}
<div class="card">
    <h2>📄 Gestionar Recursos PDF</h2>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}" class="active">Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}">Videos</a>
    <a href="{{ url_for('admin_noticias') }}">Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}">Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}">Lecciones</a>
    <a href="{{ url_for('admin_libros') }}">Libros</a>
    <a href="{{ url_for('admin_info') }}">Información</a>
    <a href="{{ url_for('admin_categorias') }}">Categorías</a>
</div>

<div class="card">
    <h3>➕ Agregar Nuevo Recurso</h3>
    <form method="POST" action="{{ url_for('admin_recursos') }}">
        <div class="form-group">
            <label for="titulo">Título:</label>
            <input type="text" id="titulo" name="titulo" required>
        </div>
        
        <div class="form-group">
            <label for="descripcion">Descripción:</label>
            <textarea id="descripcion" name="descripcion" required></textarea>
        </div>
        
        <div class="form-group">
            <label for="categoria">Categoría:</label>
            <select id="categoria" name="categoria" required>
                {% for cat in data.categorias %}
                <option value="{{ cat }}">{{ cat }}</option>
                {% endfor %}
            </select>
        </div>
        
        <div class="form-group">
            <label for="url">URL del PDF:</label>
            <input type="url" id="url" name="url" required placeholder="https://ejemplo.com/archivo.pdf">
        </div>
        
        <button type="submit" class="btn">Agregar Recurso</button>
    </form>
</div>

<div class="card">
    <h3>📋 Lista de Recursos</h3>
    {% if data.recursos %}
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Categoría</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for recurso in data.recursos %}
                <tr>
                    <td>{{ recurso.titulo }}</td>
                    <td><span class="badge">{{ recurso.categoria }}</span></td>
                    <td>{{ recurso.fecha }}</td>
                    <td>
                        <a href="{{ recurso.url }}" target="_blank" class="btn" style="padding: 0.5rem 1rem;">Ver</a>
                        <form method="POST" action="{{ url_for('delete_recurso', index=loop.index0) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger" style="padding: 0.5rem 1rem;" onclick="return confirm('¿Eliminar este recurso?')">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <p>No hay recursos agregados.</p>
    {% endif %}
</div>
{% endblock %}
'''

ADMIN_VIDEOS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Gestionar Videos - Admin{% endblock %}
{% block content %}
<div class="card">
    <h2>🎥 Gestionar Videos</h2>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}">Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}" class="active">Videos</a>
    <a href="{{ url_for('admin_noticias') }}">Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}">Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}">Lecciones</a>
    <a href="{{ url_for('admin_libros') }}">Libros</a>
    <a href="{{ url_for('admin_info') }}">Información</a>
    <a href="{{ url_for('admin_categorias') }}">Categorías</a>
</div>

<div class="card">
    <h3>➕ Agregar Nuevo Video</h3>
    <p style="color: #6b7280; margin-bottom: 1rem;">
        💡 <strong>Consejo:</strong> Para YouTube, usa el formato: https://www.youtube.com/embed/ID_DEL_VIDEO
    </p>
    <form method="POST" action="{{ url_for('admin_videos') }}">
        <div class="form-group">
            <label for="titulo">Título:</label>
            <input type="text" id="titulo" name="titulo" required>
        </div>
        
        <div class="form-group">
            <label for="descripcion">Descripción:</label>
            <textarea id="descripcion" name="descripcion" required></textarea>
        </div>
        
        <div class="form-group">
            <label for="categoria">Categoría:</label>
            <select id="categoria" name="categoria" required>
                {% for cat in data.categorias %}
                <option value="{{ cat }}">{{ cat }}</option>
                {% endfor %}
            </select>
        </div>
        
        <div class="form-group">
            <label for="url">URL del Video (embed):</label>
            <input type="url" id="url" name="url" required placeholder="https://www.youtube.com/embed/ID_VIDEO">
        </div>
        
        <button type="submit" class="btn">Agregar Video</button>
    </form>
</div>

<div class="card">
    <h3>📋 Lista de Videos</h3>
    {% if data.videos %}
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Categoría</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for video in data.videos %}
                <tr>
                    <td>{{ video.titulo }}</td>
                    <td><span class="badge">{{ video.categoria }}</span></td>
                    <td>{{ video.fecha }}</td>
                    <td>
                        <a href="{{ video.url }}" target="_blank" class="btn" style="padding: 0.5rem 1rem;">Ver</a>
                        <form method="POST" action="{{ url_for('delete_video', index=loop.index0) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger" style="padding: 0.5rem 1rem;" onclick="return confirm('¿Eliminar este video?')">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <p>No hay videos agregados.</p>
    {% endif %}
</div>
{% endblock %}
'''

ADMIN_NOTICIAS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Gestionar Noticias - Admin{% endblock %}
{% block content %}
<div class="card">
    <h2>📰 Gestionar Noticias</h2>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}">Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}">Videos</a>
    <a href="{{ url_for('admin_noticias') }}" class="active">Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}">Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}">Lecciones</a>
    <a href="{{ url_for('admin_libros') }}">Libros</a>
    <a href="{{ url_for('admin_info') }}">Información</a>
    <a href="{{ url_for('admin_categorias') }}">Categorías</a>
</div>

<div class="card">
    <h3>➕ Agregar Nueva Noticia</h3>
    <form method="POST" action="{{ url_for('admin_noticias') }}">
        <div class="form-group">
            <label for="titulo">Título:</label>
            <input type="text" id="titulo" name="titulo" required>
        </div>
        
        <div class="form-group">
            <label for="autor">Autor:</label>
            <input type="text" id="autor" name="autor" required>
        </div>
        
        <div class="form-group">
            <label for="contenido">Contenido:</label>
            <textarea id="contenido" name="contenido" required style="min-height: 200px;"></textarea>
        </div>
        
        <button type="submit" class="btn">Publicar Noticia</button>
    </form>
</div>

<div class="card">
    <h3>📋 Lista de Noticias</h3>
    {% if data.noticias %}
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Autor</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for noticia in data.noticias %}
                <tr>
                    <td>{{ noticia.titulo }}</td>
                    <td>{{ noticia.autor }}</td>
                    <td>{{ noticia.fecha }}</td>
                    <td>
                        <form method="POST" action="{{ url_for('delete_noticia', index=loop.index0) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger" style="padding: 0.5rem 1rem;" onclick="return confirm('¿Eliminar esta noticia?')">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <p>No hay noticias publicadas.</p>
    {% endif %}
</div>
{% endblock %}
'''

ADMIN_DEVOCIONALES_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Gestionar Devocionales - Admin{% endblock %}
{% block content %}
<div class="card">
    <h2>🙏 Gestionar Devocionales</h2>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}">Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}">Videos</a>
    <a href="{{ url_for('admin_noticias') }}">Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}" class="active">Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}">Lecciones</a>
    <a href="{{ url_for('admin_libros') }}">Libros</a>
    <a href="{{ url_for('admin_info') }}">Información</a>
    <a href="{{ url_for('admin_categorias') }}">Categorías</a>
</div>

<div class="card">
    <h3>➕ Agregar Nuevo Devocional</h3>
    <form method="POST" action="{{ url_for('admin_devocionales') }}">
        <div class="form-group">
            <label for="titulo">Título:</label>
            <input type="text" id="titulo" name="titulo" required>
        </div>
        
        <div class="form-group">
            <label for="versiculo">Versículo Bíblico (referencia):</label>
            <input type="text" id="versiculo" name="versiculo" required placeholder="Juan 3:16">
        </div>
        
        <div class="form-group">
            <label for="texto_biblico">Texto Bíblico:</label>
            <textarea id="texto_biblico" name="texto_biblico" required></textarea>
        </div>
        
        <div class="form-group">
            <label for="reflexion">Reflexión:</label>
            <textarea id="reflexion" name="reflexion" required style="min-height: 200px;"></textarea>
        </div>
        
        <button type="submit" class="btn">Publicar Devocional</button>
    </form>
</div>

<div class="card">
    <h3>📋 Lista de Devocionales</h3>
    {% if data.devocionales %}
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Versículo</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for devocional in data.devocionales %}
                <tr>
                    <td>{{ devocional.titulo }}</td>
                    <td>{{ devocional.versiculo }}</td>
                    <td>{{ devocional.fecha }}</td>
                    <td>
                        <form method="POST" action="{{ url_for('delete_devocional', index=loop.index0) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger" style="padding: 0.5rem 1rem;" onclick="return confirm('¿Eliminar este devocional?')">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <p>No hay devocionales publicados.</p>
    {% endif %}
</div>
{% endblock %}
'''

ADMIN_LECCIONES_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Gestionar Lecciones - Admin{% endblock %}
{% block content %}
<div class="card">
    <h2>📖 Gestionar Lecciones de Escuela Sabática</h2>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}">Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}">Videos</a>
    <a href="{{ url_for('admin_noticias') }}">Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}">Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}" class="active">Lecciones</a>
    <a href="{{ url_for('admin_libros') }}">Libros</a>
    <a href="{{ url_for('admin_info') }}">Información</a>
    <a href="{{ url_for('admin_categorias') }}">Categorías</a>
</div>

<div class="card">
    <h3>➕ Agregar Nueva Lección</h3>
    <form method="POST" action="{{ url_for('admin_lecciones') }}">
        <div class="form-group">
            <label for="titulo">Título:</label>
            <input type="text" id="titulo" name="titulo" required>
        </div>
        
        <div class="form-group">
            <label for="descripcion">Descripción:</label>
            <textarea id="descripcion" name="descripcion" required></textarea>
        </div>
        
        <div class="form-group">
            <label for="categoria">Categoría:</label>
            <select id="categoria" name="categoria" required>
                {% for cat in data.categorias %}
                <option value="{{ cat }}">{{ cat }}</option>
                {% endfor %}
            </select>
        </div>
        
        <div class="form-group">
            <label for="trimestre">Trimestre:</label>
            <input type="text" id="trimestre" name="trimestre" required placeholder="1er Trimestre 2024">
        </div>
        
        <div class="form-group">
            <label for="url">URL del PDF:</label>
            <input type="url" id="url" name="url" required placeholder="https://ejemplo.com/leccion.pdf">
        </div>
        
        <button type="submit" class="btn">Agregar Lección</button>
    </form>
</div>

<div class="card">
    <h3>📋 Lista de Lecciones</h3>
    {% if data.lecciones %}
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Categoría</th>
                    <th>Trimestre</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for leccion in data.lecciones %}
                <tr>
                    <td>{{ leccion.titulo }}</td>
                    <td><span class="badge">{{ leccion.categoria }}</span></td>
                    <td>{{ leccion.trimestre }}</td>
                    <td>{{ leccion.fecha }}</td>
                    <td>
                        <a href="{{ leccion.url }}" target="_blank" class="btn" style="padding: 0.5rem 1rem;">Ver</a>
                        <form method="POST" action="{{ url_for('delete_leccion', index=loop.index0) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger" style="padding: 0.5rem 1rem;" onclick="return confirm('¿Eliminar esta lección?')">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <p>No hay lecciones agregadas.</p>
    {% endif %}
</div>
{% endblock %}
'''

ADMIN_LIBROS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Gestionar Libros - Admin{% endblock %}
{% block content %}
<div class="card">
    <h2>📚 Gestionar Biblioteca de Libros</h2>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}">Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}">Videos</a>
    <a href="{{ url_for('admin_noticias') }}">Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}">Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}">Lecciones</a>
    <a href="{{ url_for('admin_libros') }}" class="active">Libros</a>
    <a href="{{ url_for('admin_info') }}">Información</a>
    <a href="{{ url_for('admin_categorias') }}">Categorías</a>
</div>

<div class="card">
    <h3>➕ Agregar Nuevo Libro</h3>
    <form method="POST" action="{{ url_for('admin_libros') }}">
        <div class="form-group">
            <label for="titulo">Título:</label>
            <input type="text" id="titulo" name="titulo" required>
        </div>
        
        <div class="form-group">
            <label for="autor">Autor:</label>
            <input type="text" id="autor" name="autor" required>
        </div>
        
        <div class="form-group">
            <label for="descripcion">Descripción:</label>
            <textarea id="descripcion" name="descripcion" required></textarea>
        </div>
        
        <div class="form-group">
            <label for="categoria">Categoría:</label>
            <select id="categoria" name="categoria" required>
                {% for cat in data.categorias %}
                <option value="{{ cat }}">{{ cat }}</option>
                {% endfor %}
            </select>
        </div>
        
        <div class="form-group">
            <label for="url">URL del Libro (PDF):</label>
            <input type="url" id="url" name="url" required placeholder="https://ejemplo.com/libro.pdf">
        </div>
        
        <button type="submit" class="btn">Agregar Libro</button>
    </form>
</div>

<div class="card">
    <h3>📋 Lista de Libros</h3>
    {% if data.libros %}
    <div class="table-responsive">
        <table>
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Autor</th>
                    <th>Categoría</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for libro in data.libros %}
                <tr>
                    <td>{{ libro.titulo }}</td>
                    <td>{{ libro.autor }}</td>
                    <td><span class="badge">{{ libro.categoria }}</span></td>
                    <td>{{ libro.fecha }}</td>
                    <td>
                        <a href="{{ libro.url }}" target="_blank" class="btn" style="padding: 0.5rem 1rem;">Ver</a>
                        <form method="POST" action="{{ url_for('delete_libro', index=loop.index0) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger" style="padding: 0.5rem 1rem;" onclick="return confirm('¿Eliminar este libro?')">Eliminar</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <p>No hay libros agregados.</p>
    {% endif %}
</div>
{% endblock %}
'''

ADMIN_INFO_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Gestionar Información - Admin{% endblock %}
{% block content %}
<div class="card">
    <h2>📍 Gestionar Información de Contacto</h2>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}">Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}">Videos</a>
    <a href="{{ url_for('admin_noticias') }}">Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}">Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}">Lecciones</a>
    <a href="{{ url_for('admin_libros') }}">Libros</a>
    <a href="{{ url_for('admin_info') }}" class="active">Información</a>
    <a href="{{ url_for('admin_categorias') }}">Categorías</a>
</div>

<div class="card">
    <h3>✏️ Actualizar Información</h3>
    <form method="POST" action="{{ url_for('admin_info') }}">
        <div class="form-group">
            <label for="direccion">Dirección:</label>
            <input type="text" id="direccion" name="direccion" value="{{ data.informacion.direccion }}" required>
        </div>
        
        <div class="form-group">
            <label for="telefono">Teléfono:</label>
            <input type="text" id="telefono" name="telefono" value="{{ data.informacion.telefono }}" required>
        </div>
        
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" value="{{ data.informacion.email }}" required>
        </div>
        
        <div class="form-group">
            <label for="horario">Horario de Atención:</label>
            <input type="text" id="horario" name="horario" value="{{ data.informacion.horario }}" required>
        </div>
        
        <button type="submit" class="btn">Actualizar Información</button>
    </form>
</div>
{% endblock %}
'''

ADMIN_CATEGORIAS_TEMPLATE = '''
{% extends "base.html" %}
{% block title %}Gestionar Categorías - Admin{% endblock %}
{% block content %}
<div class="card">
    <h2>🏷️ Gestionar Categorías</h2>
</div>

<div class="admin-nav">
    <a href="{{ url_for('admin_dashboard') }}">Dashboard</a>
    <a href="{{ url_for('admin_recursos') }}">Recursos PDF</a>
    <a href="{{ url_for('admin_videos') }}">Videos</a>
    <a href="{{ url_for('admin_noticias') }}">Noticias</a>
    <a href="{{ url_for('admin_devocionales') }}">Devocionales</a>
    <a href="{{ url_for('admin_lecciones') }}">Lecciones</a>
    <a href="{{ url_for('admin_libros') }}">Libros</a>
    <a href="{{ url_for('admin_info') }}">Información</a>
    <a href="{{ url_for('admin_categorias') }}" class="active">Categorías</a>
</div>

<div class="card">
    <h3>➕ Agregar Nueva Categoría</h3>
    <form method="POST" action="{{ url_for('admin_categorias') }}">
        <div class="form-group">
            <label for="categoria">Nombre de la Categoría:</label>
            <input type="text" id="categoria" name="categoria" required>
        </div>
        
        <button type="submit" name="action" value="add" class="btn">Agregar Categoría</button>
    </form>
</div>

<div class="card">
    <h3>📋 Lista de Categorías</h3>
    {% if data.categorias %}
    <div class="grid">
        {% for cat in data.categorias %}
        <div class="resource-item">
            <h3>{{ cat }}</h3>
            <form method="POST" action="{{ url_for('admin_categorias') }}" style="margin-top: 1rem;">
                <input type="hidden" name="categoria" value="{{ cat }}">
                <button type="submit" name="action" value="delete" class="btn btn-danger" onclick="return confirm('¿Eliminar esta categoría? Esto no eliminará los recursos asociados.')">Eliminar</button>
            </form>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p>No hay categorías creadas.</p>
    {% endif %}
</div>
{% endblock %}
'''

# Rutas públicas
@app.route('/')
def index():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', INDEX_TEMPLATE), data=data)

@app.route('/recursos')
def recursos():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', RECURSOS_TEMPLATE), data=data)

@app.route('/videos')
def videos():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', VIDEOS_TEMPLATE), data=data)

@app.route('/noticias')
def noticias():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', NOTICIAS_TEMPLATE), data=data)

@app.route('/devocionales')
def devocionales():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', DEVOCIONALES_TEMPLATE), data=data)

@app.route('/lecciones')
def lecciones():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', LECCIONES_TEMPLATE), data=data)

@app.route('/libros')
def libros():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', LIBROS_TEMPLATE), data=data)

@app.route('/contacto')
def contacto():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', CONTACTO_TEMPLATE), data=data)

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if check_password_hash(ADMIN_PASSWORD, password):
            session['admin_logged_in'] = True
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Contraseña incorrecta', 'error')
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', LOGIN_TEMPLATE))

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('index'))

# Rutas de administración
@app.route('/admin')
@login_required
def admin_dashboard():
    data = load_data()
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_DASHBOARD_TEMPLATE), data=data, section='dashboard')

@app.route('/admin/recursos', methods=['GET', 'POST'])
@login_required
def admin_recursos():
    data = load_data()
    if request.method == 'POST':
        nuevo_recurso = {
            'titulo': request.form.get('titulo'),
            'descripcion': request.form.get('descripcion'),
            'categoria': request.form.get('categoria'),
            'url': request.form.get('url'),
            'fecha': datetime.now().strftime('%Y-%m-%d')
        }
        data['recursos'].insert(0, nuevo_recurso)
        save_data(data)
        flash('Recurso agregado exitosamente', 'success')
        return redirect(url_for('admin_recursos'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_RECURSOS_TEMPLATE), data=data, section='recursos')

@app.route('/admin/recursos/delete/<int:index>', methods=['POST'])
@login_required
def delete_recurso(index):
    data = load_data()
    if 0 <= index < len(data['recursos']):
        data['recursos'].pop(index)
        save_data(data)
        flash('Recurso eliminado', 'success')
    return redirect(url_for('admin_recursos'))

@app.route('/admin/videos', methods=['GET', 'POST'])
@login_required
def admin_videos():
    data = load_data()
    if request.method == 'POST':
        nuevo_video = {
            'titulo': request.form.get('titulo'),
            'descripcion': request.form.get('descripcion'),
            'categoria': request.form.get('categoria'),
            'url': request.form.get('url'),
            'fecha': datetime.now().strftime('%Y-%m-%d')
        }
        data['videos'].insert(0, nuevo_video)
        save_data(data)
        flash('Video agregado exitosamente', 'success')
        return redirect(url_for('admin_videos'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_VIDEOS_TEMPLATE), data=data, section='videos')

@app.route('/admin/videos/delete/<int:index>', methods=['POST'])
@login_required
def delete_video(index):
    data = load_data()
    if 0 <= index < len(data['videos']):
        data['videos'].pop(index)
        save_data(data)
        flash('Video eliminado', 'success')
    return redirect(url_for('admin_videos'))

@app.route('/admin/noticias', methods=['GET', 'POST'])
@login_required
def admin_noticias():
    data = load_data()
    if request.method == 'POST':
        nueva_noticia = {
            'titulo': request.form.get('titulo'),
            'autor': request.form.get('autor'),
            'contenido': request.form.get('contenido'),
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        data['noticias'].insert(0, nueva_noticia)
        save_data(data)
        flash('Noticia publicada exitosamente', 'success')
        return redirect(url_for('admin_noticias'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_NOTICIAS_TEMPLATE), data=data, section='noticias')

@app.route('/admin/noticias/delete/<int:index>', methods=['POST'])
@login_required
def delete_noticia(index):
    data = load_data()
    if 0 <= index < len(data['noticias']):
        data['noticias'].pop(index)
        save_data(data)
        flash('Noticia eliminada', 'success')
    return redirect(url_for('admin_noticias'))

@app.route('/admin/devocionales', methods=['GET', 'POST'])
@login_required
def admin_devocionales():
    data = load_data()
    if request.method == 'POST':
        nuevo_devocional = {
            'titulo': request.form.get('titulo'),
            'versiculo': request.form.get('versiculo'),
            'texto_biblico': request.form.get('texto_biblico'),
            'reflexion': request.form.get('reflexion'),
            'fecha': datetime.now().strftime('%Y-%m-%d')
        }
        data['devocionales'].insert(0, nuevo_devocional)
        save_data(data)
        flash('Devocional publicado exitosamente', 'success')
        return redirect(url_for('admin_devocionales'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_DEVOCIONALES_TEMPLATE), data=data, section='devocionales')

@app.route('/admin/devocionales/delete/<int:index>', methods=['POST'])
@login_required
def delete_devocional(index):
    data = load_data()
    if 0 <= index < len(data['devocionales']):
        data['devocionales'].pop(index)
        save_data(data)
        flash('Devocional eliminado', 'success')
    return redirect(url_for('admin_devocionales'))

@app.route('/admin/lecciones', methods=['GET', 'POST'])
@login_required
def admin_lecciones():
    data = load_data()
    if request.method == 'POST':
        nueva_leccion = {
            'titulo': request.form.get('titulo'),
            'descripcion': request.form.get('descripcion'),
            'categoria': request.form.get('categoria'),
            'trimestre': request.form.get('trimestre'),
            'url': request.form.get('url'),
            'fecha': datetime.now().strftime('%Y-%m-%d')
        }
        data['lecciones'].insert(0, nueva_leccion)
        save_data(data)
        flash('Lección agregada exitosamente', 'success')
        return redirect(url_for('admin_lecciones'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_LECCIONES_TEMPLATE), data=data, section='lecciones')

@app.route('/admin/lecciones/delete/<int:index>', methods=['POST'])
@login_required
def delete_leccion(index):
    data = load_data()
    if 0 <= index < len(data['lecciones']):
        data['lecciones'].pop(index)
        save_data(data)
        flash('Lección eliminada', 'success')
    return redirect(url_for('admin_lecciones'))

@app.route('/admin/libros', methods=['GET', 'POST'])
@login_required
def admin_libros():
    data = load_data()
    if request.method == 'POST':
        nuevo_libro = {
            'titulo': request.form.get('titulo'),
            'autor': request.form.get('autor'),
            'descripcion': request.form.get('descripcion'),
            'categoria': request.form.get('categoria'),
            'url': request.form.get('url'),
            'fecha': datetime.now().strftime('%Y-%m-%d')
        }
        data['libros'].insert(0, nuevo_libro)
        save_data(data)
        flash('Libro agregado exitosamente', 'success')
        return redirect(url_for('admin_libros'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_LIBROS_TEMPLATE), data=data, section='libros')

@app.route('/admin/libros/delete/<int:index>', methods=['POST'])
@login_required
def delete_libro(index):
    data = load_data()
    if 0 <= index < len(data['libros']):
        data['libros'].pop(index)
        save_data(data)
        flash('Libro eliminado', 'success')
    return redirect(url_for('admin_libros'))

@app.route('/admin/info', methods=['GET', 'POST'])
@login_required
def admin_info():
    data = load_data()
    if request.method == 'POST':
        data['informacion'] = {
            'direccion': request.form.get('direccion'),
            'telefono': request.form.get('telefono'),
            'email': request.form.get('email'),
            'horario': request.form.get('horario')
        }
        save_data(data)
        flash('Información actualizada exitosamente', 'success')
        return redirect(url_for('admin_info'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_INFO_TEMPLATE), data=data, section='info')

@app.route('/admin/categorias', methods=['GET', 'POST'])
@login_required
def admin_categorias():
    data = load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        categoria = request.form.get('categoria')
        
        if action == 'add' and categoria and categoria not in data['categorias']:
            data['categorias'].append(categoria)
            save_data(data)
            flash('Categoría agregada exitosamente', 'success')
        elif action == 'delete' and categoria in data['categorias']:
            data['categorias'].remove(categoria)
            save_data(data)
            flash('Categoría eliminada', 'success')
        
        return redirect(url_for('admin_categorias'))
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', ADMIN_CATEGORIAS_TEMPLATE), data=data, section='categorias')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)