# app.py - Sistema Completo Departamento Espíritu de Profecía Misión Villa Perla
from flask import Flask, render_template_string, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

ADMIN_PASSWORD = generate_password_hash('jose123')
DATA_FILE = 'data.json'

def init_data():
    return {
        'recursos': [],
        'videos': [],
        'noticias': [],
        'eventos': [],
        'libro_ano': {
            'titulo': 'El Conflicto de los Siglos',
            'autor': 'Elena G. de White',
            'descripcion': 'Una obra monumental que traza la historia del gran conflicto entre el bien y el mal desde sus orígenes hasta su culminación.',
            'url': 'https://www.ejemplo.com/libro.pdf',
            'cuestionario_url': 'https://www.ejemplo.com/cuestionario.pdf'
        },
        'quienes_somos': {
            'titulo': 'Departamento de Espíritu de Profecía',
            'historia': 'El Departamento de Espíritu de Profecía de la Misión Villa Perla fue establecido con el propósito de promover el estudio y la difusión de los escritos inspirados de Elena G. de White.',
            'mision': 'Fomentar el estudio diario de la Biblia y los escritos del Espíritu de Profecía, promoviendo un avivamiento y reforma espiritual.',
            'vision': 'Cada miembro de iglesia arraigado en la Palabra de Dios y el Espíritu de Profecía, preparándose para la segunda venida de Cristo.',
            'objetivos': '1. Distribuir libros del Espíritu de Profecía\n2. Organizar seminarios y talleres\n3. Capacitar líderes\n4. Promover la lectura diaria'
        },
        'informacion': {
            'direccion': 'Misión Villa Perla, Calle Principal',
            'telefono': '+53 58604308',
            'email': 'prjoseluisgzsantana@villaperla.org',
            'horario': 'Lunes a Viernes: 8:00 AM - 5:00 PM',
            'coordinador': 'Pr. Jose Luis Gonzales Santana',
            'facebook': 'https://facebook.com/espirituprofecia',
            'youtube': 'https://youtube.com/@espirituprofecia'
        },
        'categorias_recursos': ['Infantil', 'Adolescentes', 'Jóvenes', 'Adultos', 'Matrimonios', 'Familias', 'Líderes', 'Escuela Sabática']
    }

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            defaults = init_data()
            for key in defaults:
                if key not in data:
                    data[key] = defaults[key]
            return data
    return init_data()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# CSS Global
CSS = '''
<style>
    :root {
        --primary: #1a237e;
        --primary-light: #283593;
        --primary-dark: #0d1642;
        --secondary: #c5a55a;
        --secondary-light: #d4af37;
        --accent: #2e7d32;
        --accent-light: #388e3c;
        --bg-light: #f5f5f5;
        --bg-white: #ffffff;
        --text-dark: #212121;
        --text-light: #ffffff;
        --danger: #c62828;
        --warning: #f57f17;
        --info: #0277bd;
        --shadow: 0 2px 8px rgba(0,0,0,0.1);
        --shadow-lg: 0 4px 16px rgba(0,0,0,0.2);
        --radius: 12px;
        --transition: all 0.3s ease;
        --font-main: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
        font-family: var(--font-main);
        background: var(--bg-light);
        color: var(--text-dark);
        line-height: 1.6;
    }
    
    /* Top Bar */
    .top-bar {
        background: var(--primary-dark);
        color: var(--text-light);
        padding: 0.5rem 0;
        font-size: 0.85rem;
    }
    .top-bar-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }
    .top-bar a { color: var(--text-light); text-decoration: none; margin: 0 8px; }
    .top-bar i { margin-right: 5px; color: var(--secondary); }
    .top-bar a:hover { color: var(--secondary); }
    
    /* Header */
    header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        color: white;
        padding: 1rem 0;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: var(--shadow-lg);
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
    .logo { display: flex; align-items: center; gap: 15px; }
    .logo-icon { font-size: 2.5rem; color: var(--secondary); }
    .logo-text h1 { font-size: 1.3rem; font-weight: 700; letter-spacing: 1px; }
    .logo-text p { font-size: 0.8rem; opacity: 0.9; }
    
    /* Navegación */
    nav ul { list-style: none; display: flex; gap: 0.3rem; flex-wrap: wrap; }
    nav a {
        color: white;
        text-decoration: none;
        padding: 0.5rem 0.8rem;
        border-radius: 25px;
        transition: var(--transition);
        font-weight: 500;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    nav a:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
    
    .container { max-width: 1200px; margin: 2rem auto; padding: 0 20px; min-height: 60vh; }
    
    /* Hero */
    .hero {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, var(--accent) 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: var(--radius);
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    .hero h1 { font-size: 2.8rem; margin-bottom: 1rem; position: relative; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .hero p { font-size: 1.2rem; opacity: 0.95; position: relative; }
    
    /* Cards */
    .card {
        background: var(--bg-white);
        border-radius: var(--radius);
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
        transition: var(--transition);
        border-top: 4px solid var(--secondary);
    }
    .card:hover { box-shadow: var(--shadow-lg); transform: translateY(-3px); }
    .card h2 { color: var(--primary); margin-bottom: 1rem; font-size: 1.6rem; }
    .card h3 { color: var(--primary-light); margin: 1rem 0 0.5rem; }
    
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
    .grid-2 { grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); }
    .grid-4 { grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); }
    
    /* Botones */
    .btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 0.75rem 1.5rem;
        background: var(--primary);
        color: white;
        text-decoration: none;
        border-radius: 25px;
        border: none;
        cursor: pointer;
        font-weight: 600;
        transition: var(--transition);
        font-size: 0.95rem;
    }
    .btn:hover { background: var(--primary-light); transform: translateY(-2px); box-shadow: var(--shadow); }
    .btn-accent { background: var(--accent); }
    .btn-accent:hover { background: var(--accent-light); }
    .btn-secondary { background: var(--secondary); color: var(--text-dark); }
    .btn-secondary:hover { background: var(--secondary-light); }
    .btn-danger { background: var(--danger); }
    .btn-danger:hover { background: #b71c1c; }
    .btn-sm { padding: 0.5rem 1rem; font-size: 0.85rem; }
    .btn-lg { padding: 1rem 2rem; font-size: 1.1rem; }
    
    /* Forms */
    .form-group { margin-bottom: 1.5rem; }
    label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: var(--primary); }
    input, textarea, select {
        width: 100%;
        padding: 0.85rem 1rem;
        border: 2px solid #e0e0e0;
        border-radius: 25px;
        font-size: 1rem;
        transition: var(--transition);
        font-family: inherit;
    }
    textarea { border-radius: 15px; min-height: 120px; resize: vertical; }
    input:focus, textarea:focus, select:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(26,35,126,0.1);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        background: var(--primary);
        color: white;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .badge-secondary { background: var(--secondary); color: var(--text-dark); }
    .badge-accent { background: var(--accent); }
    
    /* Resource Item */
    .resource-item {
        background: var(--bg-white);
        padding: 1.5rem;
        border-radius: var(--radius);
        border-left: 5px solid var(--secondary);
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        transition: var(--transition);
    }
    .resource-item:hover { box-shadow: var(--shadow-lg); }
    .resource-meta { color: #757575; font-size: 0.9rem; margin: 0.5rem 0; display: flex; gap: 15px; flex-wrap: wrap; }
    
    /* Tables */
    .table-responsive { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; background: white; border-radius: var(--radius); overflow: hidden; }
    th, td { padding: 1rem; text-align: left; border-bottom: 1px solid #e0e0e0; }
    th { background: var(--primary); color: white; font-weight: 600; }
    tr:hover { background: #f5f5f5; }
    
    /* Alerts */
    .alert {
        padding: 1rem 1.5rem;
        border-radius: 25px;
        margin-bottom: 1rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .alert-success { background: #e8f5e9; color: #2e7d32; border-left: 4px solid #2e7d32; }
    .alert-error { background: #ffebee; color: #c62828; border-left: 4px solid #c62828; }
    
    /* Admin Nav */
    .admin-nav {
        background: var(--bg-white);
        padding: 1rem;
        border-radius: var(--radius);
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .admin-nav a {
        padding: 0.5rem 1rem;
        background: var(--bg-light);
        color: var(--text-dark);
        text-decoration: none;
        border-radius: 20px;
        font-weight: 500;
        transition: var(--transition);
        font-size: 0.9rem;
    }
    .admin-nav a:hover, .admin-nav a.active { background: var(--primary); color: white; }
    
    /* Video */
    .video-wrapper {
        position: relative;
        padding-bottom: 56.25%;
        height: 0;
        overflow: hidden;
        border-radius: var(--radius);
        margin: 1rem 0;
    }
    .video-wrapper iframe {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        border: none;
    }
    
    /* Stats */
    .stat-card {
        text-align: center;
        padding: 2rem;
    }
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        color: var(--primary);
    }
    .stat-label { color: #757575; font-size: 1rem; }
    
    /* Footer */
    footer {
        background: var(--primary);
        color: white;
        padding: 3rem 0 1rem;
        margin-top: 3rem;
    }
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
    }
    .footer-section h3 { color: var(--secondary-light); margin-bottom: 1rem; }
    .footer-section p, .footer-section a { color: #bdbdbd; margin: 0.5rem 0; display: block; text-decoration: none; }
    .footer-section a:hover { color: var(--secondary); }
    .footer-bottom {
        text-align: center;
        padding-top: 2rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        color: #9e9e9e;
    }
    
    /* Social Icons */
    .social-icons { display: flex; gap: 1rem; margin-top: 1rem; }
    .social-icons a {
        width: 40px; height: 40px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
        transition: var(--transition);
    }
    .social-icons a:hover { background: var(--secondary); transform: translateY(-3px); }
    
    /* Search */
    .search-box {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .search-box input {
        flex: 1;
        padding: 0.75rem 1.5rem;
        border: 2px solid #e0e0e0;
        border-radius: 25px;
        font-size: 1rem;
    }
    
    /* Timeline */
    .timeline {
        position: relative;
        padding: 2rem 0;
    }
    .timeline-item {
        padding: 1rem 0 1rem 3rem;
        border-left: 3px solid var(--secondary);
        position: relative;
        margin-bottom: 1rem;
    }
    .timeline-item::before {
        content: '';
        width: 15px; height: 15px;
        background: var(--secondary);
        border-radius: 50%;
        position: absolute;
        left: -9px;
        top: 1.5rem;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-content { flex-direction: column; gap: 1rem; }
        nav ul { justify-content: center; }
        .grid, .grid-2, .grid-4 { grid-template-columns: 1fr; }
        .hero h1 { font-size: 1.8rem; }
        .hero { padding: 2rem 1rem; }
        .card { padding: 1.2rem; }
        .top-bar-content { justify-content: center; text-align: center; }
        .stat-number { font-size: 2rem; }
    }
    
    .fade-in { animation: fadeIn 0.5s ease; }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
'''

def build_page(content_html, data=None):
    if data is None:
        data = load_data()
    
    info = data['informacion']
    
    nav = f'''
    <li><a href="{url_for('index')}"><i class="fas fa-home"></i> Inicio</a></li>
    <li><a href="{url_for('quienes_somos')}"><i class="fas fa-users"></i> Quiénes Somos</a></li>
    <li><a href="{url_for('recursos')}"><i class="fas fa-file-pdf"></i> Recursos</a></li>
    <li><a href="{url_for('videos')}"><i class="fas fa-video"></i> Videos</a></li>
    <li><a href="{url_for('libro_ano')}"><i class="fas fa-book"></i> Libro del Año</a></li>
    <li><a href="{url_for('eventos')}"><i class="fas fa-calendar"></i> Eventos</a></li>
    <li><a href="{url_for('contacto')}"><i class="fas fa-address-card"></i> Contacto</a></li>
    '''
    if session.get('admin_logged_in'):
        nav += f'''<li><a href="{url_for('admin_dashboard')}"><i class="fas fa-cog"></i> Admin</a></li>
    <li><a href="{url_for('logout')}"><i class="fas fa-sign-out-alt"></i> Salir</a></li>'''
    
    # CORRECCIÓN: usar flask.get_flashed_messages en lugar de flash.get_flashed_messages
    from flask import get_flashed_messages
    flash_html = ''
    messages = get_flashed_messages(with_categories=True)
    if messages:
        for cat, msg in messages:
            icon = 'check-circle' if cat == 'success' else 'exclamation-circle'
            flash_html += f'<div class="alert alert-{cat} fade-in"><i class="fas fa-{icon}"></i> {msg}</div>'
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Espíritu de Profecía - Misión Villa Perla</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    {CSS}
</head>
<body>
    <div class="top-bar">
        <div class="top-bar-content">
            <span><i class="fas fa-phone"></i> {info['telefono']} | <i class="fas fa-envelope"></i> {info['email']}</span>
            <span>
                <a href="{info.get('facebook', '#')}"><i class="fab fa-facebook"></i></a>
                <a href="{info.get('youtube', '#')}"><i class="fab fa-youtube"></i></a>
                <a href="mailto:{info['email']}"><i class="fas fa-envelope"></i></a>
            </span>
        </div>
    </div>
    <header>
        <div class="header-content">
            <div class="logo">
                <i class="fas fa-book-open logo-icon"></i>
                <div class="logo-text">
                    <h1>Espíritu de Profecía</h1>
                    <p>Misión Villa Perla</p>
                </div>
            </div>
            <nav><ul>{nav}</ul></nav>
        </div>
    </header>
    <div class="container">{flash_html}{content_html}</div>
    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h3><i class="fas fa-church"></i> Espíritu de Profecía</h3>
                <p>Departamento dedicado a promover el estudio de los escritos inspirados en la Misión Villa Perla.</p>
                <div class="social-icons">
                    <a href="{info.get('facebook', '#')}"><i class="fab fa-facebook-f"></i></a>
                    <a href="{info.get('youtube', '#')}"><i class="fab fa-youtube"></i></a>
                    <a href="mailto:{info['email']}"><i class="fas fa-envelope"></i></a>
                </div>
            </div>
            <div class="footer-section">
                <h3>Secciones</h3>
                <a href="{url_for('recursos')}"><i class="fas fa-chevron-right"></i> Recursos PDF</a>
                <a href="{url_for('videos')}"><i class="fas fa-chevron-right"></i> Videos</a>
                <a href="{url_for('libro_ano')}"><i class="fas fa-chevron-right"></i> Libro del Año</a>
                <a href="{url_for('eventos')}"><i class="fas fa-chevron-right"></i> Eventos</a>
            </div>
            <div class="footer-section">
                <h3>Contacto</h3>
                <p><i class="fas fa-map-marker-alt"></i> {info['direccion']}</p>
                <p><i class="fas fa-phone"></i> {info['telefono']}</p>
                <p><i class="fas fa-envelope"></i> {info['email']}</p>
                <p><i class="fas fa-clock"></i> {info['horario']}</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; {datetime.now().year} Departamento de Espíritu de Profecía - Misión Villa Perla. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>'''
    return html
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Espíritu de Profecía - Misión Villa Perla</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    {CSS}
</head>
<body>
    <div class="top-bar">
        <div class="top-bar-content">
            <span><i class="fas fa-phone"></i> {info['telefono']} | <i class="fas fa-envelope"></i> {info['email']}</span>
            <span>
                <a href="{info.get('facebook', '#')}"><i class="fab fa-facebook"></i></a>
                <a href="{info.get('youtube', '#')}"><i class="fab fa-youtube"></i></a>
                <a href="mailto:{info['email']}"><i class="fas fa-envelope"></i></a>
            </span>
        </div>
    </div>
    <header>
        <div class="header-content">
            <div class="logo">
                <i class="fas fa-book-open logo-icon"></i>
                <div class="logo-text">
                    <h1>Espíritu de Profecía</h1>
                    <p>Misión Villa Perla</p>
                </div>
            </div>
            <nav><ul>{nav}</ul></nav>
        </div>
    </header>
    <div class="container">{flash_html}{content_html}</div>
    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h3><i class="fas fa-church"></i> Espíritu de Profecía</h3>
                <p>Departamento dedicado a promover el estudio de los escritos inspirados en la Misión Villa Perla.</p>
                <div class="social-icons">
                    <a href="{info.get('facebook', '#')}"><i class="fab fa-facebook-f"></i></a>
                    <a href="{info.get('youtube', '#')}"><i class="fab fa-youtube"></i></a>
                    <a href="mailto:{info['email']}"><i class="fas fa-envelope"></i></a>
                </div>
            </div>
            <div class="footer-section">
                <h3>Secciones</h3>
                <a href="{url_for('recursos')}"><i class="fas fa-chevron-right"></i> Recursos PDF</a>
                <a href="{url_for('videos')}"><i class="fas fa-chevron-right"></i> Videos</a>
                <a href="{url_for('libro_ano')}"><i class="fas fa-chevron-right"></i> Libro del Año</a>
                <a href="{url_for('eventos')}"><i class="fas fa-chevron-right"></i> Eventos</a>
            </div>
            <div class="footer-section">
                <h3>Contacto</h3>
                <p><i class="fas fa-map-marker-alt"></i> {info['direccion']}</p>
                <p><i class="fas fa-phone"></i> {info['telefono']}</p>
                <p><i class="fas fa-envelope"></i> {info['email']}</p>
                <p><i class="fas fa-clock"></i> {info['horario']}</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; {datetime.now().year} Departamento de Espíritu de Profecía - Misión Villa Perla. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>'''
    return html

# ==================== RUTAS PÚBLICAS ====================

@app.route('/')
def index():
    data = load_data()
    content = f'''
    <div class="hero">
        <h1><i class="fas fa-dove"></i> Espíritu de Profecía</h1>
        <p>Promoviendo el estudio de los escritos inspirados en la Misión Villa Perla</p>
        <div style="margin-top:2rem;position:relative;">
            <a href="{url_for('recursos')}" class="btn btn-secondary btn-lg"><i class="fas fa-book-reader"></i> Explorar Recursos</a>
            <a href="{url_for('quienes_somos')}" class="btn btn-lg" style="background:rgba(255,255,255,0.2);margin-left:1rem;"><i class="fas fa-info-circle"></i> Conócenos</a>
        </div>
    </div>
    
    <div class="grid grid-4">
        <div class="card stat-card fade-in">
            <i class="fas fa-file-pdf" style="font-size:3rem;color:var(--danger);"></i>
            <p class="stat-number">{len(data['recursos'])}</p>
            <p class="stat-label">Recursos PDF</p>
        </div>
        <div class="card stat-card fade-in">
            <i class="fas fa-video" style="font-size:3rem;color:var(--primary);"></i>
            <p class="stat-number">{len(data['videos'])}</p>
            <p class="stat-label">Videos</p>
        </div>
        <div class="card stat-card fade-in">
            <i class="fas fa-calendar-alt" style="font-size:3rem;color:var(--accent);"></i>
            <p class="stat-number">{len(data['eventos'])}</p>
            <p class="stat-label">Eventos</p>
        </div>
        <div class="card stat-card fade-in">
            <i class="fas fa-users" style="font-size:3rem;color:var(--secondary);"></i>
            <p class="stat-number">{len(data['categorias_recursos'])}</p>
            <p class="stat-label">Categorías</p>
        </div>
    </div>

    <div class="grid grid-2">
        <div class="card fade-in">
            <h2><i class="fas fa-file-pdf" style="color:var(--danger);"></i> Recursos PDF</h2>
            <p>Materiales de estudio, guías y documentos organizados por categorías para descargar.</p>
            <a href="{url_for('recursos')}" class="btn btn-accent btn-sm"><i class="fas fa-download"></i> Ver Recursos</a>
        </div>
        <div class="card fade-in">
            <h2><i class="fas fa-video" style="color:var(--primary);"></i> Videos</h2>
            <p>Sermones, seminarios y estudios bíblicos en video para tu crecimiento espiritual.</p>
            <a href="{url_for('videos')}" class="btn btn-accent btn-sm"><i class="fas fa-play"></i> Ver Videos</a>
        </div>
        <div class="card fade-in" style="background:linear-gradient(135deg,#fff8e1,#fff3e0);">
            <h2><i class="fas fa-book" style="color:var(--secondary);"></i> Libro del Año</h2>
            <p><strong>{data['libro_ano']['titulo']}</strong> - {data['libro_ano']['autor']}</p>
            <p>{data['libro_ano']['descripcion'][:150]}...</p>
            <a href="{url_for('libro_ano')}" class="btn btn-secondary btn-sm"><i class="fas fa-book-open"></i> Ver Libro</a>
        </div>
        <div class="card fade-in">
            <h2><i class="fas fa-calendar-alt" style="color:var(--accent);"></i> Eventos</h2>
            <p>Calendario de actividades, seminarios y capacitaciones del departamento.</p>
            <a href="{url_for('eventos')}" class="btn btn-accent btn-sm"><i class="fas fa-calendar-check"></i> Ver Eventos</a>
        </div>
    </div>

    <div class="card fade-in">
        <h2><i class="fas fa-newspaper"></i> Últimas Noticias y Eventos</h2>'''
    
    if data['eventos']:
        for e in data['eventos'][:3]:
            content += f'''<div class="resource-item">
            <h3>{e['titulo']}</h3>
            <div class="resource-meta">
                <span><i class="fas fa-calendar"></i> {e['fecha']}</span>
                <span><i class="fas fa-clock"></i> {e['hora']}</span>
                <span><i class="fas fa-map-marker-alt"></i> {e['lugar']}</span>
            </div>
            <p>{e['descripcion'][:150]}...</p>
        </div>'''
    else:
        content += '<p style="text-align:center;color:#757575;">No hay eventos programados actualmente.</p>'
    
    content += '</div>'
    
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/quienes-somos')
def quienes_somos():
    data = load_data()
    qs = data['quienes_somos']
    content = f'''
    <div class="card">
        <h2><i class="fas fa-users"></i> {qs['titulo']}</h2>
    </div>
    
    <div class="grid grid-2">
        <div class="card">
            <h3><i class="fas fa-history" style="color:var(--secondary);"></i> Nuestra Historia</h3>
            <p style="white-space:pre-line;line-height:1.8;">{qs['historia']}</p>
        </div>
        <div class="card">
            <h3><i class="fas fa-bullseye" style="color:var(--accent);"></i> Misión</h3>
            <p style="font-size:1.1rem;line-height:1.8;">{qs['mision']}</p>
            <h3><i class="fas fa-eye" style="color:var(--primary);margin-top:1.5rem;"></i> Visión</h3>
            <p style="font-size:1.1rem;line-height:1.8;">{qs['vision']}</p>
        </div>
    </div>
    
    <div class="card">
        <h3><i class="fas fa-list-check"></i> Nuestros Objetivos</h3>
        <p style="white-space:pre-line;line-height:2;font-size:1.1rem;">{qs['objetivos']}</p>
    </div>
    
    <div class="card" style="background:linear-gradient(135deg,#e8eaf6,#c5cae9);">
        <h3><i class="fas fa-bible"></i> Base Bíblica</h3>
        <p style="font-style:italic;font-size:1.1rem;">"Y el dragón se llenó de ira contra la mujer; y se fue a hacer guerra contra el resto de la descendencia de ella, los que guardan los mandamientos de Dios y tienen el testimonio de Jesucristo." - Apocalipsis 12:17</p>
        <p style="margin-top:1rem;">Creemos que el don de profecía es una de las características identificadoras de la iglesia remanente.</p>
    </div>
    
    <div class="card">
        <h3><i class="fas fa-user-tie"></i> Nuestro Equipo</h3>
        <div class="grid">
            <div class="resource-item">
                <h4>Coordinador</h4>
                <p style="font-size:1.2rem;"><strong>{data['informacion']['coordinador']}</strong></p>
                <p class="resource-meta"><i class="fas fa-phone"></i> {data['informacion']['telefono']}</p>
                <p class="resource-meta"><i class="fas fa-envelope"></i> {data['informacion']['email']}</p>
            </div>
        </div>
    </div>
    '''
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/recursos')
def recursos():
    data = load_data()
    content = '''
    <div class="card">
        <h2><i class="fas fa-file-pdf" style="color:var(--danger);"></i> Recursos PDF</h2>
        <p>Materiales de estudio organizados por categorías para descargar y compartir.</p>
    </div>
    
    <div class="search-box">
        <input type="text" id="searchInput" placeholder="🔍 Buscar recursos por título o descripción..." onkeyup="filterResources()">
    </div>
    '''
    
    for categoria in data['categorias_recursos']:
        recursos_cat = [r for r in data['recursos'] if r['categoria'] == categoria]
        if recursos_cat:
            items = ''
            for r in recursos_cat:
                items += f'''<div class="resource-item" data-search="{r['titulo'].lower()} {r['descripcion'].lower()}">
                <h4>{r['titulo']}</h4>
                <span class="badge">{r['categoria']}</span>
                <div class="resource-meta"><span><i class="fas fa-calendar"></i> {r['fecha']}</span></div>
                <p>{r['descripcion']}</p>
                <a href="{r['url']}" target="_blank" class="btn btn-accent btn-sm"><i class="fas fa-download"></i> Descargar PDF</a>
            </div>'''
            content += f'<div class="card"><h3><i class="fas fa-folder-open"></i> {categoria}</h3><div class="grid">{items}</div></div>'
    
    if not data['recursos']:
        content += '<div class="card"><p style="text-align:center;color:#757575;"><i class="fas fa-inbox" style="font-size:3rem;display:block;margin-bottom:1rem;"></i>No hay recursos disponibles.</p></div>'
    
    content += '''
    <script>
    function filterResources() {
        const query = document.getElementById('searchInput').value.toLowerCase();
        const items = document.querySelectorAll('.resource-item[data-search]');
        items.forEach(item => {
            item.style.display = item.dataset.search.includes(query) ? '' : 'none';
        });
        document.querySelectorAll('.card').forEach(card => {
            if (card.querySelector('.resource-item[data-search]')) {
                const visible = card.querySelectorAll('.resource-item[data-search][style=""]').length > 0 || 
                               !card.querySelector('.resource-item[data-search][style*="display: none"]');
            }
        });
    }
    </script>
    '''
    
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/videos')
def videos():
    data = load_data()
    content = '''
    <div class="card">
        <h2><i class="fas fa-video"></i> Biblioteca de Videos</h2>
        <p>Sermones, seminarios y estudios bíblicos en formato de video.</p>
    </div>
    '''
    
    for categoria in data['categorias_recursos']:
        videos_cat = [v for v in data['videos'] if v['categoria'] == categoria]
        if videos_cat:
            items = ''
            for v in videos_cat:
                items += f'''<div class="resource-item">
                <h4>{v['titulo']}</h4>
                <span class="badge">{v['categoria']}</span>
                <div class="resource-meta"><span><i class="fas fa-calendar"></i> {v['fecha']}</span></div>
                <p>{v['descripcion']}</p>
                <div class="video-wrapper"><iframe src="{v['url']}" allowfullscreen></iframe></div>
            </div>'''
            content += f'<div class="card"><h3><i class="fas fa-play-circle"></i> {categoria}</h3>{items}</div>'
    
    if not data['videos']:
        content += '<div class="card"><p style="text-align:center;color:#757575;"><i class="fas fa-video-slash" style="font-size:3rem;display:block;margin-bottom:1rem;"></i>No hay videos disponibles.</p></div>'
    
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/libro-del-ano')
def libro_ano():
    data = load_data()
    lb = data['libro_ano']
    content = f'''
    <div class="card" style="background:linear-gradient(135deg,#fff8e1,#fff3e0);border-left:5px solid var(--secondary);">
        <h2><i class="fas fa-book"></i> 📖 Libro del Año {datetime.now().year}</h2>'''
    
    if lb['titulo']:
        content += f'''
        <h3 style="font-size:2rem;color:var(--primary);">{lb['titulo']}</h3>
        <p style="font-size:1.2rem;"><strong>Autor:</strong> {lb['autor']}</p>
        <p style="white-space:pre-line;line-height:1.8;font-size:1.1rem;">{lb['descripcion']}</p>
        <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;">
            {f'<a href="{lb["url"]}" target="_blank" class="btn btn-lg"><i class="fas fa-download"></i> Descargar Libro (PDF)</a>' if lb.get('url') else ''}
            {f'<a href="{lb["cuestionario_url"]}" target="_blank" class="btn btn-accent btn-lg"><i class="fas fa-question-circle"></i> Descargar Cuestionario</a>' if lb.get('cuestionario_url') else ''}
        </div>'''
    else:
        content += '<p style="text-align:center;color:#757575;padding:2rem;"><i class="fas fa-book-open" style="font-size:3rem;display:block;margin-bottom:1rem;"></i>El libro del año aún no ha sido publicado.</p>'
    
    content += '</div>'
    
    if lb['titulo']:
        content += '''
        <div class="card">
            <h3><i class="fas fa-info-circle"></i> Plan de Lectura Sugerido</h3>
            <div class="timeline">
                <div class="timeline-item"><strong>Enero - Marzo:</strong> Leer los primeros 10 capítulos</div>
                <div class="timeline-item"><strong>Abril - Junio:</strong> Leer capítulos 11-20 y completar primera parte del cuestionario</div>
                <div class="timeline-item"><strong>Julio - Septiembre:</strong> Leer capítulos 21-30</div>
                <div class="timeline-item"><strong>Octubre - Diciembre:</strong> Leer capítulos restantes y completar cuestionario final</div>
            </div>
        </div>'''
    
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/eventos')
def eventos():
    data = load_data()
    content = '''
    <div class="card">
        <h2><i class="fas fa-calendar-alt"></i> Calendario de Eventos</h2>
        <p>Próximas actividades, seminarios y capacitaciones del departamento.</p>
    </div>'''
    
    if data['eventos']:
        for e in data['eventos']:
            content += f'''
            <div class="card">
                <h3>{e['titulo']}</h3>
                <div class="resource-meta">
                    <span><i class="fas fa-calendar"></i> <strong>Fecha:</strong> {e['fecha']}</span>
                    <span><i class="fas fa-clock"></i> <strong>Hora:</strong> {e['hora']}</span>
                    <span><i class="fas fa-map-marker-alt"></i> <strong>Lugar:</strong> {e['lugar']}</span>
                </div>
                <p style="white-space:pre-line;margin-top:1rem;">{e['descripcion']}</p>
                {f'<a href="{e["url"]}" target="_blank" class="btn btn-accent btn-sm" style="margin-top:1rem;"><i class="fas fa-external-link-alt"></i> Más Información</a>' if e.get('url') else ''}
            </div>'''
    else:
        content += '<div class="card"><p style="text-align:center;color:#757575;"><i class="fas fa-calendar-times" style="font-size:3rem;display:block;margin-bottom:1rem;"></i>No hay eventos programados.</p></div>'
    
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/contacto')
def contacto():
    data = load_data()
    info = data['informacion']
    content = f'''
    <div class="card"><h2><i class="fas fa-address-card"></i> Contacto</h2></div>
    
    <div class="grid grid-2">
        <div class="card">
            <h3><i class="fas fa-map-marker-alt" style="color:var(--primary);"></i> Dirección</h3>
            <p style="font-size:1.1rem;">{info['direccion']}</p>
            <h3 style="margin-top:1.5rem;"><i class="fas fa-phone" style="color:var(--accent);"></i> Teléfono</h3>
            <p style="font-size:1.1rem;"><a href="tel:{info['telefono']}" style="color:var(--text-dark);text-decoration:none;">{info['telefono']}</a></p>
            <h3 style="margin-top:1.5rem;"><i class="fas fa-envelope" style="color:var(--secondary);"></i> Email</h3>
            <p style="font-size:1.1rem;"><a href="mailto:{info['email']}" style="color:var(--primary);text-decoration:none;">{info['email']}</a></p>
            <h3 style="margin-top:1.5rem;"><i class="fas fa-clock"></i> Horario</h3>
            <p style="font-size:1.1rem;">{info['horario']}</p>
        </div>
        <div class="card">
            <h3><i class="fas fa-paper-plane"></i> Envíanos un Mensaje</h3>
            <form id="contactForm" onsubmit="sendMessage(event)">
                <div class="form-group"><label>Nombre:</label><input type="text" id="nombre" required></div>
                <div class="form-group"><label>Email:</label><input type="email" id="email" required></div>
                <div class="form-group"><label>Mensaje:</label><textarea id="mensaje" required></textarea></div>
                <button type="submit" class="btn"><i class="fas fa-paper-plane"></i> Enviar Mensaje</button>
            </form>
            <div id="formResponse" style="margin-top:1rem;"></div>
        </div>
    </div>
    
    <script>
    function sendMessage(e) {{
        e.preventDefault();
        document.getElementById('formResponse').innerHTML = '<div class="alert alert-success"><i class="fas fa-check-circle"></i> Mensaje enviado exitosamente. Te contactaremos pronto.</div>';
        document.getElementById('contactForm').reset();
    }}
    </script>
    '''
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if check_password_hash(ADMIN_PASSWORD, request.form['password']):
            session['admin_logged_in'] = True
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Contraseña incorrecta', 'error')
    data = load_data()
    content = '''
    <div class="card" style="max-width:450px;margin:4rem auto;">
        <h2><i class="fas fa-lock"></i> Acceso Administrativo</h2>
        <p style="color:#757575;margin-bottom:1.5rem;">Ingrese la contraseña para acceder al panel.</p>
        <form method="POST">
            <div class="form-group"><label>Contraseña:</label><input type="password" name="password" required></div>
            <button type="submit" class="btn" style="width:100%;justify-content:center;"><i class="fas fa-sign-in-alt"></i> Iniciar Sesión</button>
        </form>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Sesión cerrada', 'success')
    return redirect(url_for('index'))

# ==================== ADMIN ====================

@app.route('/admin')
@login_required
def admin_dashboard():
    data = load_data()
    content = f'''
    <div class="card"><h2><i class="fas fa-tachometer-alt"></i> Panel de Administración</h2></div>
    <div class="admin-nav">
        <a href="{url_for('admin_dashboard')}" class="active">Dashboard</a>
        <a href="{url_for('admin_quienes_somos')}">Quiénes Somos</a>
        <a href="{url_for('admin_recursos')}">Recursos PDF</a>
        <a href="{url_for('admin_videos')}">Videos</a>
        <a href="{url_for('admin_libro_ano')}">Libro del Año</a>
        <a href="{url_for('admin_eventos')}">Eventos</a>
        <a href="{url_for('admin_info')}">Información</a>
        <a href="{url_for('admin_categorias')}">Categorías</a>
    </div>
    <div class="grid grid-4">
        <div class="card stat-card"><i class="fas fa-file-pdf" style="font-size:3rem;color:var(--danger);"></i><p class="stat-number">{len(data['recursos'])}</p><p class="stat-label">Recursos</p></div>
        <div class="card stat-card"><i class="fas fa-video" style="font-size:3rem;color:var(--primary);"></i><p class="stat-number">{len(data['videos'])}</p><p class="stat-label">Videos</p></div>
        <div class="card stat-card"><i class="fas fa-calendar" style="font-size:3rem;color:var(--accent);"></i><p class="stat-number">{len(data['eventos'])}</p><p class="stat-label">Eventos</p></div>
        <div class="card stat-card"><i class="fas fa-tags" style="font-size:3rem;color:var(--secondary);"></i><p class="stat-number">{len(data['categorias_recursos'])}</p><p class="stat-label">Categorías</p></div>
    </div>
    <div class="card">
        <h3>Acciones Rápidas</h3>
        <a href="{url_for('admin_recursos')}" class="btn btn-sm"><i class="fas fa-plus"></i> Agregar Recurso</a>
        <a href="{url_for('admin_videos')}" class="btn btn-sm"><i class="fas fa-plus"></i> Agregar Video</a>
        <a href="{url_for('admin_eventos')}" class="btn btn-sm"><i class="fas fa-plus"></i> Agregar Evento</a>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

# Admin Quiénes Somos
@app.route('/admin/quienes-somos', methods=['GET', 'POST'])
@login_required
def admin_quienes_somos():
    data = load_data()
    if request.method == 'POST':
        data['quienes_somos'] = {
            'titulo': request.form['titulo'],
            'historia': request.form['historia'],
            'mision': request.form['mision'],
            'vision': request.form['vision'],
            'objetivos': request.form['objetivos']
        }
        save_data(data)
        flash('Información actualizada', 'success')
        return redirect(url_for('admin_quienes_somos'))
    qs = data['quienes_somos']
    content = f'''
    <div class="card"><h2>Editar Quiénes Somos</h2></div>
    <div class="admin-nav"><a href="{url_for('admin_dashboard')}">Dashboard</a><a href="{url_for('admin_quienes_somos')}" class="active">Quiénes Somos</a></div>
    <div class="card">
        <form method="POST">
            <div class="form-group"><label>Título:</label><input type="text" name="titulo" value="{qs['titulo']}" required></div>
            <div class="form-group"><label>Historia:</label><textarea name="historia" required>{qs['historia']}</textarea></div>
            <div class="form-group"><label>Misión:</label><textarea name="mision" required>{qs['mision']}</textarea></div>
            <div class="form-group"><label>Visión:</label><textarea name="vision" required>{qs['vision']}</textarea></div>
            <div class="form-group"><label>Objetivos:</label><textarea name="objetivos" required>{qs['objetivos']}</textarea></div>
            <button type="submit" class="btn">Actualizar</button>
        </form>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

# Admin Recursos
@app.route('/admin/recursos', methods=['GET', 'POST'])
@login_required
def admin_recursos():
    data = load_data()
    if request.method == 'POST':
        data['recursos'].insert(0, {
            'titulo': request.form['titulo'],
            'descripcion': request.form['descripcion'],
            'categoria': request.form['categoria'],
            'url': request.form['url'],
            'fecha': datetime.now().strftime('%Y-%m-%d')
        })
        save_data(data)
        flash('Recurso agregado', 'success')
        return redirect(url_for('admin_recursos'))
    
    cat_opts = ''.join([f'<option value="{c}">{c}</option>' for c in data['categorias_recursos']])
    rows = ''
    for i, r in enumerate(data['recursos']):
        rows += f'''<tr>
            <td>{r['titulo']}</td>
            <td><span class="badge">{r['categoria']}</span></td>
            <td>{r['fecha']}</td>
            <td>
                <a href="{r['url']}" target="_blank" class="btn btn-sm">Ver</a>
                <form method="POST" action="{url_for('delete_recurso', index=i)}" style="display:inline;">
                    <button class="btn btn-danger btn-sm" onclick="return confirm('¿Eliminar?')">Eliminar</button>
                </form>
            </td>
        </tr>'''
    
    content = f'''
    <div class="card"><h2>Gestionar Recursos PDF</h2></div>
    <div class="admin-nav"><a href="{url_for('admin_dashboard')}">Dashboard</a><a href="{url_for('admin_recursos')}" class="active">Recursos</a></div>
    <div class="card">
        <h3>Agregar Recurso</h3>
        <form method="POST">
            <div class="form-group"><label>Título:</label><input type="text" name="titulo" required></div>
            <div class="form-group"><label>Descripción:</label><textarea name="descripcion" required></textarea></div>
            <div class="form-group"><label>Categoría:</label><select name="categoria" required>{cat_opts}</select></div>
            <div class="form-group"><label>URL PDF:</label><input type="url" name="url" required></div>
            <button type="submit" class="btn">Agregar</button>
        </form>
    </div>
    <div class="card">
        <h3>Lista ({len(data['recursos'])})</h3>
        <div class="table-responsive"><table><thead><tr><th>Título</th><th>Categoría</th><th>Fecha</th><th>Acciones</th></tr></thead><tbody>{rows or '<tr><td colspan="4">Sin recursos</td></tr>'}</tbody></table></div>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/admin/recursos/delete/<int:index>', methods=['POST'])
@login_required
def delete_recurso(index):
    data = load_data()
    if 0 <= index < len(data['recursos']):
        data['recursos'].pop(index)
        save_data(data)
        flash('Recurso eliminado', 'success')
    return redirect(url_for('admin_recursos'))

# Admin Videos
@app.route('/admin/videos', methods=['GET', 'POST'])
@login_required
def admin_videos():
    data = load_data()
    if request.method == 'POST':
        data['videos'].insert(0, {
            'titulo': request.form['titulo'],
            'descripcion': request.form['descripcion'],
            'categoria': request.form['categoria'],
            'url': request.form['url'],
            'fecha': datetime.now().strftime('%Y-%m-%d')
        })
        save_data(data)
        flash('Video agregado', 'success')
        return redirect(url_for('admin_videos'))
    
    cat_opts = ''.join([f'<option value="{c}">{c}</option>' for c in data['categorias_recursos']])
    rows = ''
    for i, v in enumerate(data['videos']):
        rows += f'''<tr>
            <td>{v['titulo']}</td>
            <td><span class="badge">{v['categoria']}</span></td>
            <td>{v['fecha']}</td>
            <td>
                <form method="POST" action="{url_for('delete_video', index=i)}" style="display:inline;">
                    <button class="btn btn-danger btn-sm" onclick="return confirm('¿Eliminar?')">Eliminar</button>
                </form>
            </td>
        </tr>'''
    
    content = f'''
    <div class="card"><h2>Gestionar Videos</h2></div>
    <div class="admin-nav"><a href="{url_for('admin_dashboard')}">Dashboard</a><a href="{url_for('admin_videos')}" class="active">Videos</a></div>
    <div class="card">
        <h3>Agregar Video</h3>
        <p style="color:#757575;">URL embed: https://www.youtube.com/embed/ID</p>
        <form method="POST">
            <div class="form-group"><label>Título:</label><input type="text" name="titulo" required></div>
            <div class="form-group"><label>Descripción:</label><textarea name="descripcion" required></textarea></div>
            <div class="form-group"><label>Categoría:</label><select name="categoria" required>{cat_opts}</select></div>
            <div class="form-group"><label>URL Embed:</label><input type="url" name="url" required></div>
            <button type="submit" class="btn">Agregar</button>
        </form>
    </div>
    <div class="card">
        <h3>Lista ({len(data['videos'])})</h3>
        <div class="table-responsive"><table><thead><tr><th>Título</th><th>Categoría</th><th>Fecha</th><th>Acciones</th></tr></thead><tbody>{rows or '<tr><td colspan="4">Sin videos</td></tr>'}</tbody></table></div>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/admin/videos/delete/<int:index>', methods=['POST'])
@login_required
def delete_video(index):
    data = load_data()
    if 0 <= index < len(data['videos']):
        data['videos'].pop(index)
        save_data(data)
        flash('Video eliminado', 'success')
    return redirect(url_for('admin_videos'))

# Admin Libro del Año
@app.route('/admin/libro-ano', methods=['GET', 'POST'])
@login_required
def admin_libro_ano():
    data = load_data()
    if request.method == 'POST':
        data['libro_ano'] = {
            'titulo': request.form['titulo'],
            'autor': request.form['autor'],
            'descripcion': request.form['descripcion'],
            'url': request.form['url'],
            'cuestionario_url': request.form['cuestionario_url']
        }
        save_data(data)
        flash('Libro actualizado', 'success')
        return redirect(url_for('admin_libro_ano'))
    lb = data['libro_ano']
    content = f'''
    <div class="card"><h2>Libro del Año</h2></div>
    <div class="admin-nav"><a href="{url_for('admin_dashboard')}">Dashboard</a><a href="{url_for('admin_libro_ano')}" class="active">Libro</a></div>
    <div class="card">
        <form method="POST">
            <div class="form-group"><label>Título:</label><input type="text" name="titulo" value="{lb['titulo']}" required></div>
            <div class="form-group"><label>Autor:</label><input type="text" name="autor" value="{lb['autor']}" required></div>
            <div class="form-group"><label>Descripción:</label><textarea name="descripcion" required>{lb['descripcion']}</textarea></div>
            <div class="form-group"><label>URL Libro:</label><input type="url" name="url" value="{lb.get('url','')}"></div>
            <div class="form-group"><label>URL Cuestionario:</label><input type="url" name="cuestionario_url" value="{lb.get('cuestionario_url','')}"></div>
            <button type="submit" class="btn">Guardar</button>
        </form>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

# Admin Eventos
@app.route('/admin/eventos', methods=['GET', 'POST'])
@login_required
def admin_eventos():
    data = load_data()
    if request.method == 'POST':
        data['eventos'].insert(0, {
            'titulo': request.form['titulo'],
            'fecha': request.form['fecha'],
            'hora': request.form['hora'],
            'lugar': request.form['lugar'],
            'descripcion': request.form['descripcion'],
            'url': request.form.get('url', '')
        })
        save_data(data)
        flash('Evento agregado', 'success')
        return redirect(url_for('admin_eventos'))
    
    rows = ''
    for i, e in enumerate(data['eventos']):
        rows += f'''<tr>
            <td>{e['titulo']}</td>
            <td>{e['fecha']}</td>
            <td>{e['lugar']}</td>
            <td>
                <form method="POST" action="{url_for('delete_evento', index=i)}" style="display:inline;">
                    <button class="btn btn-danger btn-sm" onclick="return confirm('¿Eliminar?')">Eliminar</button>
                </form>
            </td>
        </tr>'''
    
    content = f'''
    <div class="card"><h2>Gestionar Eventos</h2></div>
    <div class="admin-nav"><a href="{url_for('admin_dashboard')}">Dashboard</a><a href="{url_for('admin_eventos')}" class="active">Eventos</a></div>
    <div class="card">
        <h3>Agregar Evento</h3>
        <form method="POST">
            <div class="form-group"><label>Título:</label><input type="text" name="titulo" required></div>
            <div class="form-group"><label>Fecha:</label><input type="text" name="fecha" placeholder="15 de Diciembre, 2024" required></div>
            <div class="form-group"><label>Hora:</label><input type="text" name="hora" placeholder="10:00 AM" required></div>
            <div class="form-group"><label>Lugar:</label><input type="text" name="lugar" required></div>
            <div class="form-group"><label>Descripción:</label><textarea name="descripcion" required></textarea></div>
            <div class="form-group"><label>URL (opcional):</label><input type="url" name="url"></div>
            <button type="submit" class="btn">Agregar</button>
        </form>
    </div>
    <div class="card">
        <h3>Lista ({len(data['eventos'])})</h3>
        <div class="table-responsive"><table><thead><tr><th>Título</th><th>Fecha</th><th>Lugar</th><th>Acciones</th></tr></thead><tbody>{rows or '<tr><td colspan="4">Sin eventos</td></tr>'}</tbody></table></div>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

@app.route('/admin/eventos/delete/<int:index>', methods=['POST'])
@login_required
def delete_evento(index):
    data = load_data()
    if 0 <= index < len(data['eventos']):
        data['eventos'].pop(index)
        save_data(data)
        flash('Evento eliminado', 'success')
    return redirect(url_for('admin_eventos'))

# Admin Info
@app.route('/admin/info', methods=['GET', 'POST'])
@login_required
def admin_info():
    data = load_data()
    if request.method == 'POST':
        data['informacion'] = {
            'direccion': request.form['direccion'],
            'telefono': request.form['telefono'],
            'email': request.form['email'],
            'horario': request.form['horario'],
            'coordinador': request.form['coordinador'],
            'facebook': request.form['facebook'],
            'youtube': request.form['youtube']
        }
        save_data(data)
        flash('Información actualizada', 'success')
        return redirect(url_for('admin_info'))
    info = data['informacion']
    content = f'''
    <div class="card"><h2>Información General</h2></div>
    <div class="admin-nav"><a href="{url_for('admin_dashboard')}">Dashboard</a><a href="{url_for('admin_info')}" class="active">Info</a></div>
    <div class="card">
        <form method="POST">
            <div class="form-group"><label>Dirección:</label><input type="text" name="direccion" value="{info['direccion']}" required></div>
            <div class="form-group"><label>Teléfono:</label><input type="text" name="telefono" value="{info['telefono']}" required></div>
            <div class="form-group"><label>Email:</label><input type="email" name="email" value="{info['email']}" required></div>
            <div class="form-group"><label>Horario:</label><input type="text" name="horario" value="{info['horario']}" required></div>
            <div class="form-group"><label>Coordinador:</label><input type="text" name="coordinador" value="{info['coordinador']}" required></div>
            <div class="form-group"><label>Facebook URL:</label><input type="url" name="facebook" value="{info.get('facebook','')}"></div>
            <div class="form-group"><label>YouTube URL:</label><input type="url" name="youtube" value="{info.get('youtube','')}"></div>
            <button type="submit" class="btn">Actualizar</button>
        </form>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

# Admin Categorías
@app.route('/admin/categorias', methods=['GET', 'POST'])
@login_required
def admin_categorias():
    data = load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        cat = request.form.get('categoria', '').strip()
        if action == 'add' and cat and cat not in data['categorias_recursos']:
            data['categorias_recursos'].append(cat)
            save_data(data)
            flash('Categoría agregada', 'success')
        elif action == 'delete' and cat in data['categorias_recursos']:
            data['categorias_recursos'].remove(cat)
            save_data(data)
            flash('Categoría eliminada', 'success')
        return redirect(url_for('admin_categorias'))
    
    cards = ''
    for cat in data['categorias_recursos']:
        cards += f'''<div class="resource-item">
            <h4>{cat}</h4>
            <form method="POST">
                <input type="hidden" name="categoria" value="{cat}">
                <button type="submit" name="action" value="delete" class="btn btn-danger btn-sm" onclick="return confirm('¿Eliminar?')">Eliminar</button>
            </form>
        </div>'''
    
    content = f'''
    <div class="card"><h2>Gestionar Categorías</h2></div>
    <div class="admin-nav"><a href="{url_for('admin_dashboard')}">Dashboard</a><a href="{url_for('admin_categorias')}" class="active">Categorías</a></div>
    <div class="card">
        <h3>Agregar</h3>
        <form method="POST">
            <div class="form-group"><label>Nombre:</label><input type="text" name="categoria" required></div>
            <button type="submit" name="action" value="add" class="btn">Agregar</button>
        </form>
    </div>
    <div class="card">
        <h3>Lista ({len(data['categorias_recursos'])})</h3>
        <div class="grid">{cards or '<p>Sin categorías</p>'}</div>
    </div>'''
    html = build_page(content, data)
    return render_template_string(html, data=data)

if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        save_data(init_data())
    app.run(debug=True, host='0.0.0.0', port=5000)
