# app.py - Sistema Espíritu de Profecía Misión Villa Perla
from flask import Flask, render_template_string, request, redirect, url_for, session, get_flashed_messages
from functools import wraps
from datetime import datetime
import json, os
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
        'eventos': [],
        'libro_ano': {'titulo':'','autor':'','descripcion':'','url':'','cuestionario_url':''},
        'quienes_somos': {
            'titulo':'Departamento de Espiritu de Profecia',
            'historia':'El Departamento de Espiritu de Profecia de la Mision Villa Perla fue establecido para promover el estudio y la difusion de los escritos inspirados de Elena G. de White.',
            'mision':'Fomentar el estudio diario de la Biblia y los escritos del Espiritu de Profecia.',
            'vision':'Cada miembro arraigado en la Palabra de Dios y el Espiritu de Profecia.',
            'objetivos':'1. Distribuir libros del Espiritu de Profecia\n2. Organizar seminarios y talleres\n3. Capacitar lideres\n4. Promover la lectura diaria'
        },
        'informacion': {
            'direccion':'Mision Villa Perla, Calle Principal #123',
            'telefono':'+53 58604308',
            'email':'prluisgzsantana@villaperla.org',
            'horario':'Lunes a Viernes: 8:00 AM - 5:00 PM',
            'coordinador':'Pr. Jose Luis Gonzales Santana',
            'facebook':'',
            'youtube':''
        },
        'categorias_recursos': ['Infantil','Adolescentes','Jovenes','Adultos','Matrimonios','Familias','Lideres','Escuela Sabatica']
    }

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r',encoding='utf-8') as f:
            data = json.load(f)
            for k in init_data():
                if k not in data: data[k] = init_data()[k]
            return data
    return init_data()

def save_data(data):
    with open(DATA_FILE,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def login_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if 'admin_logged_in' not in session: return redirect(url_for('login'))
        return f(*args,**kwargs)
    return decorated

def build_page(content, data=None):
    if not data: data = load_data()
    info = data['informacion']
    
    nav_items = [
        ('index','Inicio','home'),
        ('quienes_somos','Quienes Somos','users'),
        ('recursos','Recursos','file-pdf'),
        ('videos','Videos','video'),
        ('libro_ano','Libro del Ano','book'),
        ('eventos','Eventos','calendar'),
        ('contacto','Contacto','address-card')
    ]
    
    nav_desktop = ''
    for r, n, i in nav_items:
        nav_desktop += '<li><a href="' + url_for(r) + '">' + n + '</a></li>'
    if session.get('admin_logged_in'):
        nav_desktop += '<li><a href="' + url_for('admin_dashboard') + '">Admin</a></li>'
        nav_desktop += '<li><a href="' + url_for('logout') + '">Salir</a></li>'
    
    sidebar_items = ''
    for r, n, i in nav_items:
        sidebar_items += '<li><a href="' + url_for(r) + '"><i class="fas fa-' + i + '"></i> ' + n + '</a></li>'
    if session.get('admin_logged_in'):
        sidebar_items += '<li><a href="' + url_for('admin_dashboard') + '"><i class="fas fa-cog"></i> Admin</a></li>'
        sidebar_items += '<li><a href="' + url_for('logout') + '"><i class="fas fa-sign-out-alt"></i> Salir</a></li>'
    
    flash_html = ''
    messages = get_flashed_messages(with_categories=True)
    if messages:
        for cat, msg in messages:
            ic = 'check-circle' if cat == 'success' else 'exclamation-circle'
            flash_html += '<div class="alert alert-' + cat + ' fade"><i class="fas fa-' + ic + '"></i> ' + msg + '</div>'
    
    html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>Departamento de Educación y Espíritu de Profecía - Misión Villa Perla</title>
    <!-- Open Graph / WhatsApp / Facebook -->
<meta property="og:title" content="Departamento de Educación y Espíritu de Profecía - Misión Villa Perla">
<meta property="og:description" content="Recursos educativos, videos, libros y materiales de estudio del Departamento de Espíritu de Profecía de la Misión Villa Perla.">
<meta property="og:image" content="/favicon.ico">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://t.me/obisoftd3v">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Desarrollador @ObisoftDev!">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Departamento de Educación y Espíritu de Profecía - Misión Villa Perla">
<meta name="twitter:description" content="Recursos educativos, videos, libros y materiales de estudio.">
<meta name="twitter:image" content="/favicon.ico">

<!-- WhatsApp específico -->
<meta name="description" content="Departamento de Educación y Espíritu de Profecía de la Misión Villa Perla. Recursos, videos, libros y materiales de estudio.">
<link rel="icon" type="image/png" href="/favicon.ico">

    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700&family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
:root {
    --orange: #E8751A;
    --orange-dark: #C45D0E;
    --orange-light: #F4984A;
    --black: #1A1A1A;
    --black-light: #2D2D2D;
    --white: #FFFFFF;
    --gray-50: #FAFAFA;
    --gray-100: #F5F5F5;
    --gray-200: #E5E5E5;
    --gray-300: #D4D4D4;
    --gray-600: #666666;
    --gray-800: #333333;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
    --shadow: 0 4px 12px rgba(0,0,0,0.08);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.12);
    --radius: 4px;
    --radius-lg: 8px;
    --transition: all 0.25s ease;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Open Sans', -apple-system, sans-serif;
    background: var(--white);
    color: var(--black);
    line-height: 1.7;
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Merriweather', Georgia, serif;
    color: var(--black);
    line-height: 1.3;
}

.top-bar {
    background: var(--black);
    color: var(--white);
    padding: 10px 0;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
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
.top-bar a { color: var(--gray-300); text-decoration: none; margin: 0 10px; transition: var(--transition); }
.top-bar a:hover { color: var(--orange); }
.top-bar i { color: var(--orange); margin-right: 5px; }

header {
    background: var(--white);
    border-bottom: 3px solid var(--orange);
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: var(--shadow-sm);
}
.header-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
}
.logo-icon {
    font-size: 2rem;
    color: var(--orange);
}
.logo-text h1 {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--black);
    letter-spacing: 0.5px;
}
.logo-text p {
    font-size: 0.75rem;
    color: var(--gray-600);
    font-family: 'Open Sans', sans-serif;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.nav-desktop { display: flex; }
.nav-desktop ul {
    list-style: none;
    display: flex;
    gap: 5px;
}
.nav-desktop a {
    color: var(--black);
    text-decoration: none;
    padding: 8px 14px;
    border-radius: var(--radius);
    transition: var(--transition);
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
.nav-desktop a:hover {
    color: var(--orange);
    background: var(--gray-100);
}

.hamburger {
    display: none;
    background: none;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 8px 12px;
    cursor: pointer;
    color: var(--black);
    font-size: 1.5rem;
    transition: var(--transition);
}
.hamburger:hover { border-color: var(--orange); color: var(--orange); }

.sidebar-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.6);
    z-index: 2000;
    animation: fadeIn 0.3s;
}
.sidebar-overlay.active { display: block; }

.sidebar {
    position: fixed;
    top: 0;
    right: -320px;
    width: 300px;
    height: 100vh;
    background: var(--white);
    z-index: 2001;
    transition: right 0.3s ease;
    overflow-y: auto;
    box-shadow: -4px 0 30px rgba(0,0,0,0.2);
    padding: 20px;
}
.sidebar.active { right: 0; }
.sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid var(--orange);
    margin-bottom: 20px;
}
.sidebar-header h3 {
    font-size: 1.1rem;
    color: var(--black);
}
.sidebar-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--gray-600);
    transition: var(--transition);
}
.sidebar-close:hover { color: var(--orange); }
.sidebar ul { list-style: none; }
.sidebar ul li { border-bottom: 1px solid var(--gray-200); }
.sidebar a {
    display: block;
    padding: 14px 10px;
    color: var(--black);
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    transition: var(--transition);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.sidebar a:hover { color: var(--orange); padding-left: 20px; }
.sidebar a i { color: var(--orange); margin-right: 12px; width: 20px; text-align: center; }

.container { max-width: 1200px; margin: 2rem auto; padding: 0 20px; min-height: 60vh; }

.hero {
    background: var(--black);
    color: var(--white);
    padding: 80px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(232,117,26,0.15) 0%, transparent 50%);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 4px;
    background: var(--orange);
}
.hero h1 {
    font-size: 2.8rem;
    color: var(--white);
    margin-bottom: 1rem;
    position: relative;
}
.hero p {
    font-size: 1.1rem;
    color: var(--gray-300);
    position: relative;
    max-width: 700px;
    margin: 0 auto;
}
.hero .accent { color: var(--orange); }

.card {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: var(--transition);
}
.card:hover {
    border-color: var(--orange);
    box-shadow: var(--shadow);
}
.card h2 {
    font-size: 1.5rem;
    color: var(--black);
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--orange);
}
.card h3 {
    font-size: 1.15rem;
    color: var(--black);
    margin: 1rem 0 0.5rem;
}

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
.g2 { grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); }
.g4 { grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); }

.btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 28px;
    background: var(--orange);
    color: var(--white);
    text-decoration: none;
    border-radius: var(--radius);
    border: 2px solid var(--orange);
    cursor: pointer;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    transition: var(--transition);
    font-family: 'Open Sans', sans-serif;
}
.btn:hover { background: var(--orange-dark); border-color: var(--orange-dark); }
.btn-outline {
    background: transparent;
    color: var(--orange);
}
.btn-outline:hover { background: var(--orange); color: var(--white); }
.btn-black { background: var(--black); border-color: var(--black); }
.btn-black:hover { background: var(--black-light); }
.btn-sm { padding: 8px 18px; font-size: 0.75rem; }
.btn-lg { padding: 16px 36px; font-size: 0.95rem; }

.form-group { margin-bottom: 1.5rem; }
label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 700;
    color: var(--black);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
input, textarea, select {
    width: 100%;
    padding: 14px 16px;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius);
    font-size: 1rem;
    font-family: 'Open Sans', sans-serif;
    transition: var(--transition);
    background: var(--gray-50);
}
input:focus, textarea:focus, select:focus {
    outline: none;
    border-color: var(--orange);
    background: var(--white);
    box-shadow: 0 0 0 3px rgba(232,117,26,0.1);
}
textarea { min-height: 120px; resize: vertical; }

.badge {
    display: inline-block;
    padding: 5px 14px;
    background: var(--black);
    color: var(--white);
    border-radius: 3px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 3px;
}

.resource-item {
    background: var(--white);
    padding: 1.5rem;
    border: 1px solid var(--gray-200);
    border-left: 4px solid var(--orange);
    margin-bottom: 1rem;
    border-radius: var(--radius);
    transition: var(--transition);
}
.resource-item:hover {
    border-left-color: var(--black);
    box-shadow: var(--shadow);
}
.resource-meta {
    color: var(--gray-600);
    font-size: 0.8rem;
    margin: 0.5rem 0;
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.table-responsive { overflow-x: auto; }
table {
    width: 100%;
    border-collapse: collapse;
    background: var(--white);
    font-size: 0.9rem;
}
th, td {
    padding: 14px 16px;
    text-align: left;
    border-bottom: 1px solid var(--gray-200);
}
th {
    background: var(--black);
    color: var(--white);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.75rem;
}
tr:hover { background: var(--gray-50); }

.alert {
    padding: 16px 20px;
    border-radius: var(--radius);
    margin-bottom: 1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
}
.alert-success { background: #F0F9F0; color: #1A7A1A; border-left: 4px solid #1A7A1A; }
.alert-error { background: #FFF0F0; color: #C41E1E; border-left: 4px solid #C41E1E; }

.admin-nav {
    background: var(--gray-100);
    padding: 12px;
    border-radius: var(--radius);
    margin-bottom: 1.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}
.admin-nav a {
    padding: 8px 16px;
    background: var(--white);
    color: var(--black);
    text-decoration: none;
    border-radius: var(--radius);
    font-weight: 600;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    border: 1px solid var(--gray-200);
    transition: var(--transition);
}
.admin-nav a:hover, .admin-nav a.active {
    background: var(--orange);
    color: var(--white);
    border-color: var(--orange);
}

.video-wrapper {
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
    overflow: hidden;
    border-radius: var(--radius);
    margin: 1rem 0;
    border: 1px solid var(--gray-200);
}
.video-wrapper iframe {
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
    border: none;
}

.stat-card { text-align: center; padding: 2rem; border-top: 4px solid var(--orange); }
.stat-number { font-size: 3rem; font-weight: 700; color: var(--orange); font-family: 'Merriweather', serif; }
.stat-label { color: var(--gray-600); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0.5rem; }

.search-box { display: flex; gap: 10px; margin-bottom: 1.5rem; }
.search-box input {
    flex: 1;
    padding: 14px 20px;
    border: 2px solid var(--gray-200);
    border-radius: var(--radius);
    font-size: 0.95rem;
    background: var(--gray-50);
}
.search-box input:focus { border-color: var(--orange); background: var(--white); }

footer {
    background: var(--black);
    color: var(--gray-300);
    padding: 60px 0 20px;
    margin-top: 60px;
}
.footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 40px;
}
.footer-section h3 {
    color: var(--orange);
    margin-bottom: 20px;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.footer-section p, .footer-section a {
    color: var(--gray-600);
    margin: 8px 0;
    display: block;
    text-decoration: none;
    font-size: 0.85rem;
    transition: var(--transition);
}
.footer-section a:hover { color: var(--orange); }
.footer-bottom {
    text-align: center;
    padding-top: 30px;
    margin-top: 30px;
    border-top: 1px solid var(--gray-800);
    color: var(--gray-600);
    font-size: 0.8rem;
}
.social-icons { display: flex; gap: 12px; margin-top: 15px; }
.social-icons a {
    width: 36px; height: 36px;
    border: 1px solid var(--gray-800);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--gray-300);
    transition: var(--transition);
}
.social-icons a:hover { border-color: var(--orange); color: var(--orange); }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.fade { animation: fadeIn 0.5s ease; }

@media (max-width: 768px) {
    .nav-desktop { display: none; }
    .hamburger { display: block; }
    header { position: relative; }
    .header-content { padding: 12px 16px; }
    .grid, .g2, .g4 { grid-template-columns: 1fr; }
    .hero { padding: 50px 20px; }
    .hero h1 { font-size: 1.8rem; }
    .hero p { font-size: 0.95rem; }
    .card { padding: 1.2rem; }
    .card h2 { font-size: 1.2rem; }
    .stat-number { font-size: 2rem; }
    .container { padding: 0 16px; margin: 1.5rem auto; }
    table { font-size: 0.8rem; }
    th, td { padding: 10px 12px; }
    .sidebar { width: 280px; right: -280px; }
}

@media (min-width: 769px) {
    .sidebar, .sidebar-overlay { display: none !important; }
}
</style>
</head>
<body>

<div class="top-bar">
    <div class="top-bar-content">
        <span><i class="fas fa-phone"></i> ''' + info['telefono'] + ''' <span style="margin:0 15px">|</span> <i class="fas fa-envelope"></i> ''' + info['email'] + '''</span>
        <span>
            <a href="''' + info.get('facebook','#') + '''"><i class="fab fa-facebook-f"></i></a>
            <a href="''' + info.get('youtube','#') + '''"><i class="fab fa-youtube"></i></a>
            <a href="mailto:''' + info['email'] + '''"><i class="fas fa-envelope"></i></a>
        </span>
    </div>
</div>

<header>
    <div class="header-content">
        <a href="''' + url_for('index') + '''" class="logo">
            <i class="fas fa-book-open logo-icon"></i>
            <div class="logo-text">
                <h1>Espiritu de Profecia</h1>
                <p>Mision Villa Perla</p>
            </div>
        </a>
        <nav class="nav-desktop"><ul>''' + nav_desktop + '''</ul></nav>
        <button class="hamburger" onclick="openSidebar()" aria-label="Menu"><i class="fas fa-bars"></i></button>
    </div>
</header>

<div class="sidebar-overlay" id="sidebarOverlay" onclick="closeSidebar()"></div>
<div class="sidebar" id="sidebar">
    <div class="sidebar-header">
        <h3>Menu</h3>
        <button class="sidebar-close" onclick="closeSidebar()" aria-label="Cerrar"><i class="fas fa-times"></i></button>
    </div>
    <ul>''' + sidebar_items + '''</ul>
</div>

<div class="container">''' + flash_html + content + '''</div>

<footer>
    <div class="footer-content">
        <div class="footer-section">
            <h3>Espiritu de Profecia</h3>
            <p>Departamento dedicado a promover el estudio de los escritos inspirados en la Mision Villa Perla.</p>
            <div class="social-icons">
                <a href="''' + info.get('facebook','#') + '''"><i class="fab fa-facebook-f"></i></a>
                <a href="''' + info.get('youtube','#') + '''"><i class="fab fa-youtube"></i></a>
                <a href="mailto:''' + info['email'] + '''"><i class="fas fa-envelope"></i></a>
            </div>
        </div>
        <div class="footer-section">
            <h3>Secciones</h3>
            <a href="''' + url_for('recursos') + '''">Recursos PDF</a>
            <a href="''' + url_for('videos') + '''">Videos</a>
            <a href="''' + url_for('libro_ano') + '''">Libro del Ano</a>
            <a href="''' + url_for('eventos') + '''">Eventos</a>
        </div>
        <div class="footer-section">
            <h3>Contacto</h3>
            <p><i class="fas fa-map-marker-alt"></i> ''' + info['direccion'] + '''</p>
            <p><i class="fas fa-phone"></i> ''' + info['telefono'] + '''</p>
            <p><i class="fas fa-envelope"></i> ''' + info['email'] + '''</p>
        </div>
    </div>
    <div class="footer-bottom">
        <p>&copy; ''' + str(datetime.now().year) + ''' Espiritu de Profecia - Mision Villa Perla.</p>
    </div>
</footer>

<script>
function openSidebar() {
    document.getElementById('sidebar').classList.add('active');
    document.getElementById('sidebarOverlay').classList.add('active');
    document.body.style.overflow = 'hidden';
}
function closeSidebar() {
    document.getElementById('sidebar').classList.remove('active');
    document.getElementById('sidebarOverlay').classList.remove('active');
    document.body.style.overflow = '';
}
</script>
</body>
</html>'''
    return html

@app.route('/')
def index():
    data = load_data()
    ev = ''
    for e in data['eventos'][:3]:
        ev += '<div class="resource-item"><h4>' + e['titulo'] + '</h4><div class="resource-meta"><span><i class="fas fa-calendar"></i> ' + e['fecha'] + '</span><span><i class="fas fa-map-marker-alt"></i> ' + e['lugar'] + '</span></div><p>' + e['descripcion'][:120] + '...</p></div>'
    
    c = '<div class="hero"><h1>Departamento de<br><span class="accent">Espiritu de Profecia</span></h1><p>Promoviendo el estudio de los escritos inspirados en la Mision Villa Perla</p><div style="margin-top:2rem"><a href="' + url_for('recursos') + '" class="btn btn-lg">Explorar Recursos</a> <a href="' + url_for('quienes_somos') + '" class="btn btn-outline btn-lg">Conocenos</a></div></div>'
    
    c += '<div class="grid g4">'
    c += '<div class="card stat-card fade"><p class="stat-number">' + str(len(data['recursos'])) + '</p><p class="stat-label">Recursos</p></div>'
    c += '<div class="card stat-card fade"><p class="stat-number">' + str(len(data['videos'])) + '</p><p class="stat-label">Videos</p></div>'
    c += '<div class="card stat-card fade"><p class="stat-number">' + str(len(data['eventos'])) + '</p><p class="stat-label">Eventos</p></div>'
    c += '<div class="card stat-card fade"><p class="stat-number">' + str(len(data['categorias_recursos'])) + '</p><p class="stat-label">Categorias</p></div>'
    c += '</div>'
    
    c += '<div class="grid g2">'
    c += '<div class="card fade"><h2>Recursos PDF</h2><p>Materiales de estudio organizados por categorias para descargar.</p><a href="' + url_for('recursos') + '" class="btn btn-sm">Ver Recursos</a></div>'
    c += '<div class="card fade"><h2>Videos</h2><p>Sermones, seminarios y estudios biblicos en video.</p><a href="' + url_for('videos') + '" class="btn btn-sm">Ver Videos</a></div>'
    c += '<div class="card fade" style="border-top:4px solid var(--orange)"><h2>Libro del Ano</h2><p><strong>' + (data['libro_ano']['titulo'] or 'Proximamente') + '</strong></p><a href="' + url_for('libro_ano') + '" class="btn btn-outline btn-sm">Ver Libro</a></div>'
    c += '<div class="card fade"><h2>Eventos</h2><p>Calendario de actividades del departamento.</p><a href="' + url_for('eventos') + '" class="btn btn-sm">Ver Eventos</a></div>'
    c += '</div>'
    
    c += '<div class="card fade"><h2>Proximos Eventos</h2><div class="grid">' + (ev or '<p style="text-align:center;color:var(--gray-600)">No hay eventos programados.</p>') + '</div></div>'
    
    return render_template_string(build_page(c, data), data=data)

@app.route('/quienes-somos')
def quienes_somos():
    data = load_data()
    q = data['quienes_somos']
    c = '<div class="card"><h2>' + q['titulo'] + '</h2></div>'
    c += '<div class="grid g2">'
    c += '<div class="card"><h3>Nuestra Historia</h3><p style="white-space:pre-line;line-height:1.8">' + q['historia'] + '</p></div>'
    c += '<div class="card"><h3>Mision</h3><p style="font-size:1.1rem;line-height:1.8">' + q['mision'] + '</p><h3 style="margin-top:1.5rem">Vision</h3><p style="font-size:1.1rem;line-height:1.8">' + q['vision'] + '</p></div>'
    c += '</div>'
    c += '<div class="card"><h3>Objetivos</h3><p style="white-space:pre-line;line-height:2;font-size:1.05rem">' + q['objetivos'] + '</p></div>'
    c += '<div class="card" style="border-left:4px solid var(--orange);background:var(--gray-50)"><h3>Base Biblica</h3><p style="font-style:italic;font-size:1.1rem">"Y el dragon se lleno de ira contra la mujer; y se fue a hacer guerra contra el resto de la descendencia de ella, los que guardan los mandamientos de Dios y tienen el testimonio de Jesucristo." - Apocalipsis 12:17</p></div>'
    c += '<div class="card"><h3>Coordinador</h3><p style="font-size:1.2rem"><strong>' + data['informacion']['coordinador'] + '</strong></p><p class="resource-meta"><i class="fas fa-phone"></i> ' + data['informacion']['telefono'] + ' <span style="margin:0 10px">|</span> <i class="fas fa-envelope"></i> ' + data['informacion']['email'] + '</p></div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/recursos')
def recursos():
    data = load_data()
    items = ''
    for cat in data['categorias_recursos']:
        recs = [r for r in data['recursos'] if r['categoria'] == cat]
        if recs:
            items += '<div class="card"><h3>' + cat + '</h3><div class="grid">'
            for r in recs:
                items += '<div class="resource-item" data-search="' + r['titulo'].lower() + ' ' + r['descripcion'].lower() + '"><h4>' + r['titulo'] + '</h4><span class="badge">' + r['categoria'] + '</span><div class="resource-meta"><span><i class="fas fa-calendar"></i> ' + r['fecha'] + '</span></div><p>' + r['descripcion'] + '</p><a href="' + r['url'] + '" target="_blank" class="btn btn-sm">Descargar PDF</a></div>'
            items += '</div></div>'
    c = '<div class="card"><h2>Recursos PDF</h2><div class="search-box"><input type="text" id="s" placeholder="Buscar recursos..." onkeyup="var q=this.value.toLowerCase();document.querySelectorAll(\'.resource-item[data-search]\').forEach(function(e){e.style.display=e.dataset.search.indexOf(q)>-1?\'\':\'none\'})"></div></div>' + (items or '<div class="card"><p style="text-align:center;color:var(--gray-600)">No hay recursos disponibles.</p></div>')
    return render_template_string(build_page(c, data), data=data)

@app.route('/videos')
def videos():
    data = load_data()
    items = ''
    for cat in data['categorias_recursos']:
        vids = [v for v in data['videos'] if v['categoria'] == cat]
        if vids:
            items += '<div class="card"><h3>' + cat + '</h3>'
            for v in vids:
                items += '<div class="resource-item"><h4>' + v['titulo'] + '</h4><span class="badge">' + v['categoria'] + '</span><div class="resource-meta"><span><i class="fas fa-calendar"></i> ' + v['fecha'] + '</span></div><p>' + v['descripcion'] + '</p><div class="video-wrapper"><iframe src="' + v['url'] + '" allowfullscreen></iframe></div></div>'
            items += '</div>'
    c = '<div class="card"><h2>Biblioteca de Videos</h2><p>Sermones, seminarios y estudios biblicos en video.</p></div>' + (items or '<div class="card"><p style="text-align:center;color:var(--gray-600)">No hay videos disponibles.</p></div>')
    return render_template_string(build_page(c, data), data=data)

@app.route('/libro-del-ano')
def libro_ano():
    data = load_data()
    lb = data['libro_ano']
    c = '<div class="card" style="border-top:4px solid var(--orange);border-left:4px solid var(--orange)"><h2>Libro del Ano ' + str(datetime.now().year) + '</h2>'
    if lb['titulo']:
        c += '<h3 style="font-size:1.6rem;color:var(--orange)">' + lb['titulo'] + '</h3><p><strong>Autor:</strong> ' + lb['autor'] + '</p><p style="white-space:pre-line;line-height:1.8;margin:1.5rem 0">' + lb['descripcion'] + '</p><div style="display:flex;gap:1rem;flex-wrap:wrap">'
        if lb.get('url'): c += '<a href="' + lb['url'] + '" target="_blank" class="btn btn-lg">Descargar Libro</a>'
        if lb.get('cuestionario_url'): c += '<a href="' + lb['cuestionario_url'] + '" target="_blank" class="btn btn-outline btn-lg">Descargar Cuestionario</a>'
        c += '</div>'
    else:
        c += '<p style="text-align:center;padding:3rem;color:var(--gray-600);font-size:1.2rem">El libro del ano sera publicado proximamente.</p>'
    c += '</div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/eventos')
def eventos():
    data = load_data()
    items = ''
    for e in data['eventos']:
        items += '<div class="card"><h3>' + e['titulo'] + '</h3><div class="resource-meta"><span><i class="fas fa-calendar"></i> ' + e['fecha'] + '</span><span><i class="fas fa-clock"></i> ' + e['hora'] + '</span><span><i class="fas fa-map-marker-alt"></i> ' + e['lugar'] + '</span></div><p style="white-space:pre-line;margin-top:1rem">' + e['descripcion'] + '</p>'
        if e.get('url'): items += '<a href="' + e['url'] + '" target="_blank" class="btn btn-outline btn-sm" style="margin-top:1rem">Mas Informacion</a>'
        items += '</div>'
    c = '<div class="card"><h2>Calendario de Eventos</h2></div>' + (items or '<div class="card"><p style="text-align:center;color:var(--gray-600)">No hay eventos programados.</p></div>')
    return render_template_string(build_page(c, data), data=data)

@app.route('/contacto')
def contacto():
    data = load_data()
    info = data['informacion']
    c = '<div class="card"><h2>Contacto</h2></div><div class="grid g2">'
    c += '<div class="card">'
    c += '<p style="margin:1rem 0"><i class="fas fa-map-marker-alt" style="color:var(--orange);margin-right:10px"></i> ' + info['direccion'] + '</p>'
    c += '<p style="margin:1rem 0"><i class="fas fa-phone" style="color:var(--orange);margin-right:10px"></i> <a href="tel:' + info['telefono'] + '" style="color:var(--black)">' + info['telefono'] + '</a></p>'
    c += '<p style="margin:1rem 0"><i class="fas fa-envelope" style="color:var(--orange);margin-right:10px"></i> <a href="mailto:' + info['email'] + '" style="color:var(--orange)">' + info['email'] + '</a></p>'
    c += '<p style="margin:1rem 0"><i class="fas fa-clock" style="color:var(--orange);margin-right:10px"></i> ' + info['horario'] + '</p>'
    c += '<p style="margin:1rem 0"><i class="fas fa-user-tie" style="color:var(--orange);margin-right:10px"></i> Coordinador: ' + info['coordinador'] + '</p>'
    c += '</div>'
    c += '<div class="card"><h3>Envianos un Mensaje</h3><form onsubmit="event.preventDefault();this.insertAdjacentHTML(\'afterend\',\'<div class="alert alert-success" style="margin-top:1rem">Mensaje enviado. Te contactaremos pronto.</div>\');this.reset()"><div class="form-group"><label>Nombre</label><input type="text" required></div><div class="form-group"><label>Email</label><input type="email" required></div><div class="form-group"><label>Mensaje</label><textarea required></textarea></div><button type="submit" class="btn">Enviar Mensaje</button></form></div>'
    c += '</div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if check_password_hash(ADMIN_PASSWORD, request.form['password']):
            session['admin_logged_in'] = True
            from flask import flash; flash('Inicio de sesion exitoso', 'success')
            return redirect(url_for('admin_dashboard'))
        from flask import flash; flash('Contrasena incorrecta', 'error')
    c = '<div class="card" style="max-width:450px;margin:4rem auto"><h2>Acceso Administrativo</h2><form method="POST"><div class="form-group"><label>Contrasena</label><input type="password" name="password" required></div><button type="submit" class="btn" style="width:100%;justify-content:center">Iniciar Sesion</button></form></div>'
    return render_template_string(build_page(c), data=load_data())

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    from flask import flash; flash('Sesion cerrada', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    data = load_data()
    nav_links = [
        ("admin_dashboard","Dashboard"),("admin_quienes_somos","Quienes Somos"),
        ("admin_recursos","Recursos"),("admin_videos","Videos"),
        ("admin_libro_ano","Libro del Ano"),("admin_eventos","Eventos"),
        ("admin_info","Informacion"),("admin_categorias","Categorias")
    ]
    n = '<div class="admin-nav">'
    for r, t in nav_links:
        active = ' active' if r == 'admin_dashboard' else ''
        n += '<a href="' + url_for(r) + '" class="' + active + '">' + t + '</a>'
    n += '</div>'
    
    s = ''
    for v, l in [(len(data['recursos']),'Recursos'),(len(data['videos']),'Videos'),(len(data['eventos']),'Eventos'),(len(data['categorias_recursos']),'Categorias')]:
        s += '<div class="card stat-card"><p class="stat-number">' + str(v) + '</p><p class="stat-label">' + l + '</p></div>'
    
    c = '<div class="card"><h2>Panel de Administracion</h2></div>' + n + '<div class="grid g4">' + s + '</div>'
    c += '<div class="card"><a href="' + url_for('admin_recursos') + '" class="btn btn-sm">+ Agregar Recurso</a> <a href="' + url_for('admin_videos') + '" class="btn btn-sm">+ Agregar Video</a> <a href="' + url_for('admin_eventos') + '" class="btn btn-sm">+ Agregar Evento</a></div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/admin/quienes-somos', methods=['GET','POST'])
@login_required
def admin_quienes_somos():
    data = load_data()
    if request.method == 'POST':
        data['quienes_somos'] = {k:request.form[k] for k in ['titulo','historia','mision','vision','objetivos']}
        save_data(data)
        from flask import flash; flash('Informacion actualizada', 'success')
        return redirect(url_for('admin_quienes_somos'))
    q = data['quienes_somos']
    c = '<div class="card"><h2>Editar Quienes Somos</h2></div><div class="admin-nav"><a href="' + url_for('admin_dashboard') + '">Dashboard</a><a href="' + url_for('admin_quienes_somos') + '" class="active">Quienes Somos</a></div><div class="card"><form method="POST">'
    for k in ['titulo','historia','mision','vision','objetivos']:
        c += '<div class="form-group"><label>' + k.title() + '</label>'
        if k in ['historia','mision','vision','objetivos']:
            c += '<textarea name="' + k + '" required>' + q[k] + '</textarea>'
        else:
            c += '<input type="text" name="' + k + '" value="' + q[k] + '" required>'
        c += '</div>'
    c += '<button type="submit" class="btn">Actualizar</button></form></div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/admin/recursos', methods=['GET','POST'])
@login_required
def admin_recursos():
    data = load_data()
    if request.method == 'POST':
        data['recursos'].insert(0, {
            'titulo':request.form['titulo'],
            'descripcion':request.form['descripcion'],
            'categoria':request.form['categoria'],
            'url':request.form['url'],
            'fecha':datetime.now().strftime('%Y-%m-%d')
        })
        save_data(data)
        from flask import flash; flash('Recurso agregado', 'success')
        return redirect(url_for('admin_recursos'))
    
    co = ''
    for c in data['categorias_recursos']:
        co += '<option>' + c + '</option>'
    
    rows = ''
    for i, r in enumerate(data['recursos']):
        rows += '<tr><td>' + r['titulo'] + '</td><td><span class="badge">' + r['categoria'] + '</span></td><td>' + r['fecha'] + '</td><td><a href="' + r['url'] + '" target="_blank" class="btn btn-sm">Ver</a> <form method="POST" action="' + url_for('delete_recurso', index=i) + '" style="display:inline"><button class="btn btn-sm" style="background:var(--black);border-color:var(--black)" onclick="return confirm(\'Eliminar?\')">Eliminar</button></form></td></tr>'
    
    c = '<div class="card"><h2>Gestionar Recursos</h2></div><div class="admin-nav"><a href="' + url_for('admin_dashboard') + '">Dashboard</a><a href="' + url_for('admin_recursos') + '" class="active">Recursos</a></div>'
    c += '<div class="card"><h3>Agregar Recurso</h3><form method="POST"><div class="form-group"><label>Titulo</label><input type="text" name="titulo" required></div><div class="form-group"><label>Descripcion</label><textarea name="descripcion" required></textarea></div><div class="form-group"><label>Categoria</label><select name="categoria" required>' + co + '</select></div><div class="form-group"><label>URL del PDF</label><input type="url" name="url" required></div><button type="submit" class="btn">Agregar Recurso</button></form></div>'
    c += '<div class="card"><h3>Lista (' + str(len(data['recursos'])) + ')</h3><div class="table-responsive"><table><thead><tr><th>Titulo</th><th>Categoria</th><th>Fecha</th><th>Acciones</th></tr></thead><tbody>' + (rows or '<tr><td colspan="4">Sin recursos</td></tr>') + '</tbody></table></div></div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/admin/recursos/delete/<int:index>', methods=['POST'])
@login_required
def delete_recurso(index):
    data = load_data()
    if 0 <= index < len(data['recursos']):
        data['recursos'].pop(index)
        save_data(data)
        from flask import flash; flash('Recurso eliminado', 'success')
    return redirect(url_for('admin_recursos'))

@app.route('/admin/videos', methods=['GET','POST'])
@login_required
def admin_videos():
    data = load_data()
    if request.method == 'POST':
        data['videos'].insert(0, {
            'titulo':request.form['titulo'],
            'descripcion':request.form['descripcion'],
            'categoria':request.form['categoria'],
            'url':request.form['url'],
            'fecha':datetime.now().strftime('%Y-%m-%d')
        })
        save_data(data)
        from flask import flash; flash('Video agregado', 'success')
        return redirect(url_for('admin_videos'))
    
    co = ''
    for c in data['categorias_recursos']:
        co += '<option>' + c + '</option>'
    
    rows = ''
    for i, v in enumerate(data['videos']):
        rows += '<tr><td>' + v['titulo'] + '</td><td><span class="badge">' + v['categoria'] + '</span></td><td>' + v['fecha'] + '</td><td><form method="POST" action="' + url_for('delete_video', index=i) + '" style="display:inline"><button class="btn btn-sm" style="background:var(--black);border-color:var(--black)" onclick="return confirm(\'Eliminar?\')">Eliminar</button></form></td></tr>'
    
    c = '<div class="card"><h2>Gestionar Videos</h2></div><div class="admin-nav"><a href="' + url_for('admin_dashboard') + '">Dashboard</a><a href="' + url_for('admin_videos') + '" class="active">Videos</a></div>'
    c += '<div class="card"><h3>Agregar Video</h3><p style="color:var(--gray-600);margin-bottom:1rem">URL embed: https://www.youtube.com/embed/ID</p><form method="POST"><div class="form-group"><label>Titulo</label><input type="text" name="titulo" required></div><div class="form-group"><label>Descripcion</label><textarea name="descripcion" required></textarea></div><div class="form-group"><label>Categoria</label><select name="categoria" required>' + co + '</select></div><div class="form-group"><label>URL Embed</label><input type="url" name="url" required></div><button type="submit" class="btn">Agregar Video</button></form></div>'
    c += '<div class="card"><h3>Lista (' + str(len(data['videos'])) + ')</h3><div class="table-responsive"><table><thead><tr><th>Titulo</th><th>Categoria</th><th>Fecha</th><th>Acciones</th></tr></thead><tbody>' + (rows or '<tr><td colspan="4">Sin videos</td></tr>') + '</tbody></table></div></div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/admin/videos/delete/<int:index>', methods=['POST'])
@login_required
def delete_video(index):
    data = load_data()
    if 0 <= index < len(data['videos']):
        data['videos'].pop(index)
        save_data(data)
        from flask import flash; flash('Video eliminado', 'success')
    return redirect(url_for('admin_videos'))

@app.route('/admin/libro-ano', methods=['GET','POST'])
@login_required
def admin_libro_ano():
    data = load_data()
    if request.method == 'POST':
        data['libro_ano'] = {k:request.form[k] for k in ['titulo','autor','descripcion','url','cuestionario_url']}
        save_data(data)
        from flask import flash; flash('Libro actualizado', 'success')
        return redirect(url_for('admin_libro_ano'))
    lb = data['libro_ano']
    c = '<div class="card"><h2>Libro del Ano</h2></div><div class="admin-nav"><a href="' + url_for('admin_dashboard') + '">Dashboard</a><a href="' + url_for('admin_libro_ano') + '" class="active">Libro del Ano</a></div><div class="card"><form method="POST">'
    for k in ['titulo','autor','descripcion','url','cuestionario_url']:
        c += '<div class="form-group"><label>' + k.title() + '</label>'
        if k == 'descripcion':
            c += '<textarea name="' + k + '" required>' + lb.get(k,'') + '</textarea>'
        else:
            t = 'url' if 'url' in k else 'text'
            c += '<input type="' + t + '" name="' + k + '" value="' + lb.get(k,'') + '" required>'
        c += '</div>'
    c += '<button type="submit" class="btn">Guardar</button></form></div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/admin/eventos', methods=['GET','POST'])
@login_required
def admin_eventos():
    data = load_data()
    if request.method == 'POST':
        data['eventos'].insert(0, {
            'titulo':request.form['titulo'],
            'fecha':request.form['fecha'],
            'hora':request.form['hora'],
            'lugar':request.form['lugar'],
            'descripcion':request.form['descripcion'],
            'url':request.form.get('url','')
        })
        save_data(data)
        from flask import flash; flash('Evento agregado', 'success')
        return redirect(url_for('admin_eventos'))
    
    rows = ''
    for i, e in enumerate(data['eventos']):
        rows += '<tr><td>' + e['titulo'] + '</td><td>' + e['fecha'] + '</td><td>' + e['lugar'] + '</td><td><form method="POST" action="' + url_for('delete_evento', index=i) + '" style="display:inline"><button class="btn btn-sm" style="background:var(--black);border-color:var(--black)" onclick="return confirm(\'Eliminar?\')">Eliminar</button></form></td></tr>'
    
    c = '<div class="card"><h2>Gestionar Eventos</h2></div><div class="admin-nav"><a href="' + url_for('admin_dashboard') + '">Dashboard</a><a href="' + url_for('admin_eventos') + '" class="active">Eventos</a></div>'
    c += '<div class="card"><h3>Agregar Evento</h3><form method="POST"><div class="form-group"><label>Titulo</label><input type="text" name="titulo" required></div><div class="form-group"><label>Fecha</label><input type="text" name="fecha" placeholder="15 de Diciembre, 2024" required></div><div class="form-group"><label>Hora</label><input type="text" name="hora" placeholder="10:00 AM" required></div><div class="form-group"><label>Lugar</label><input type="text" name="lugar" required></div><div class="form-group"><label>Descripcion</label><textarea name="descripcion" required></textarea></div><div class="form-group"><label>URL (opcional)</label><input type="url" name="url"></div><button type="submit" class="btn">Agregar Evento</button></form></div>'
    c += '<div class="card"><h3>Lista (' + str(len(data['eventos'])) + ')</h3><div class="table-responsive"><table><thead><tr><th>Titulo</th><th>Fecha</th><th>Lugar</th><th>Acciones</th></tr></thead><tbody>' + (rows or '<tr><td colspan="4">Sin eventos</td></tr>') + '</tbody></table></div></div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/admin/eventos/delete/<int:index>', methods=['POST'])
@login_required
def delete_evento(index):
    data = load_data()
    if 0 <= index < len(data['eventos']):
        data['eventos'].pop(index)
        save_data(data)
        from flask import flash; flash('Evento eliminado', 'success')
    return redirect(url_for('admin_eventos'))

@app.route('/admin/info', methods=['GET','POST'])
@login_required
def admin_info():
    data = load_data()
    if request.method == 'POST':
        data['informacion'] = {k:request.form[k] for k in ['direccion','telefono','email','horario','coordinador','facebook','youtube']}
        save_data(data)
        from flask import flash; flash('Informacion actualizada', 'success')
        return redirect(url_for('admin_info'))
    info = data['informacion']
    c = '<div class="card"><h2>Informacion General</h2></div><div class="admin-nav"><a href="' + url_for('admin_dashboard') + '">Dashboard</a><a href="' + url_for('admin_info') + '" class="active">Info</a></div><div class="card"><form method="POST">'
    for k in ['direccion','telefono','email','horario','coordinador','facebook','youtube']:
        t = 'url' if k in ['facebook','youtube'] else 'email' if k == 'email' else 'text'
        c += '<div class="form-group"><label>' + k.title() + '</label><input type="' + t + '" name="' + k + '" value="' + info.get(k,'') + '" required></div>'
    c += '<button type="submit" class="btn">Actualizar</button></form></div>'
    return render_template_string(build_page(c, data), data=data)

@app.route('/admin/categorias', methods=['GET','POST'])
@login_required
def admin_categorias():
    data = load_data()
    if request.method == 'POST':
        action = request.form.get('action')
        cat = request.form.get('categoria','').strip()
        if action == 'add' and cat and cat not in data['categorias_recursos']:
            data['categorias_recursos'].append(cat)
            save_data(data)
            from flask import flash; flash('Categoria agregada', 'success')
        elif action == 'delete' and cat in data['categorias_recursos']:
            data['categorias_recursos'].remove(cat)
            save_data(data)
            from flask import flash; flash('Categoria eliminada', 'success')
        return redirect(url_for('admin_categorias'))
    
    cards = ''
    for c in data['categorias_recursos']:
        cards += '<div class="resource-item"><h4>' + c + '</h4><form method="POST"><input type="hidden" name="categoria" value="' + c + '"><button type="submit" name="action" value="delete" class="btn btn-sm" style="background:var(--black);border-color:var(--black);margin-top:.5rem" onclick="return confirm(\'Eliminar?\')">Eliminar</button></form></div>'
    
    c = '<div class="card"><h2>Gestionar Categorias</h2></div><div class="admin-nav"><a href="' + url_for('admin_dashboard') + '">Dashboard</a><a href="' + url_for('admin_categorias') + '" class="active">Categorias</a></div>'
    c += '<div class="card"><h3>Agregar Categoria</h3><form method="POST"><div class="form-group"><label>Nombre</label><input type="text" name="categoria" required></div><button type="submit" name="action" value="add" class="btn">Agregar</button></form></div>'
    c += '<div class="card"><h3>Lista (' + str(len(data['categorias_recursos'])) + ')</h3><div class="grid">' + (cards or '<p style="text-align:center;color:var(--gray-600)">Sin categorias</p>') + '</div></div>'
    return render_template_string(build_page(c, data), data=data)

if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        save_data(init_data())
    app.run(debug=True, host='0.0.0.0', port=5000)
