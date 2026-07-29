# 🔥 WebStrike - Bug Bounty Toolkit

> **Herramienta de pentesting web enfocada en Bug Bounty**

WebStrike es una herramienta modular diseñada para automatizar el reconocimiento inicial en procesos de Bug Bounty. Su arquitectura permite añadir nuevos módulos de ataque fácilmente.

---

## 📋 Características

- ✅ **Arquitectura modular** — Añade nuevos módulos sin modificar el core
- ✅ **Reconocimiento inicial** — Análisis básico de objetivos
- ✅ **Múltiples métodos HTTP** — GET, POST, PUT, etc.
- ✅ **Detección de tecnologías** — Identifica servidores y frameworks
- ✅ **Redirecciones** — Seguimiento automático con límite
- ✅ **Headers de seguridad** — Análisis de protección del objetivo

---

## 🚀 Instalación

### Requisitos

```bash
# Python 3.6+
python3 --version
```

### Clonar repositorio

```bash
git clone https://github.com/tu-usuario/webstrike.git
cd webstrike
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Dependencias principales

```txt
requests>=2.28.0
termcolor>=2.1.0
```

---

## 📖 Uso Básico

### Sintaxis general

```bash
python3 webstrike.py -u <URL> -t <MODULO> [OPCIONES]
```

### Ejemplo mínimo

```bash
python3 webstrike.py -u https://ejemplo.com -t Basic
```

### Ejemplo con opciones

```bash
python3 webstrike.py -u https://ejemplo.com -t Basic -m POST -U "CustomAgent/1.0"
```

---

## 🎯 Opciones disponibles

| Opción | Descripción | Obligatorio |
|---|---|---|
| `-u`, `--url` | URL objetivo | ✅ Sí |
| `-t`, `--type-attack` | Módulo a ejecutar | ✅ Sí |
| `-m`, `--method` | Método HTTP (GET, POST, PUT...) | ❌ No (por defecto GET) |
| `-U`, `--user-agent` | User-Agent personalizado | ❌ No |
| `-q`, `--quiet` | Modo silencioso (sin banner) | ❌ No |

---

## 🔌 Módulos Disponibles

### 1️⃣ BasicRequestModule - `Basic`

Reconocimiento inicial del objetivo.

**Información que reporta:**

- Código de estado HTTP
- Tiempo de respuesta
- Servidor web y tecnologías detectadas
- Headers de seguridad
- Redirecciones (con seguimiento automático)
- Content-Type y Content-Length

**Ejemplo:**

```bash
python3 webstrike.py -u https://hackviser.com -t Basic
```

**Salida esperada:**

```text
[*] Status code: 200
[*] Response time: 0.088 seg
[*] Server info:
     Server: cloudflare
     Tecnologías: Cloudflare
[*] Content-Type: text/html
[*] Content-Length: 6001
```

---

## 🛡️ Casos de Uso en Bug Bounty

### 1. Reconocimiento rápido

```bash
# Análisis básico del objetivo
python3 webstrike.py -u https://target.com -t Basic
```

### 2. Diferentes métodos HTTP

```bash
# Probar con POST
python3 webstrike.py -u https://target.com/api -t Basic -m POST

# Probar con PUT
python3 webstrike.py -u https://target.com/api -t Basic -m PUT
```

### 3. Evadir WAF con User-Agent

```bash
python3 webstrike.py -u https://target.com -t Basic -U "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

### 4. Modo silencioso para scripts

```bash
python3 webstrike.py -u https://target.com -t Basic -q
```

---

## 📁 Estructura del Proyecto

```text
WebStrike/
├── webstrike.py              # Script principal
├── modules/
│   ├── __init__.py
│   ├── base_module.py        # Clase base (futuro)
│   └── basic_request.py      # Módulo Basic
├── requirements.txt
└── README.md
```

---

## 🚧 Próximos Módulos

- [ ] **SQLi** - Detección de SQL Injection
- [ ] **LFI** - Local File Inclusion
- [ ] **XSS** - Cross-Site Scripting
- [ ] **Subdomain** - Enumeración de subdominios
- [ ] **DirBuster** - Fuzzing de directorios
- [ ] **CORS** - Análisis de configuración CORS

---

## ⚠️ Limitaciones Actuales

- Solo módulo `Basic` implementado
- No soporta autenticación (próximamente)
- Sin exportación de reportes (próximamente)

---

## 📝 Notas Legales

> ⚠️ **ADVERTENCIA:** Esta herramienta está diseñada para fines educativos y de Bug Bounty. Asegúrate de tener autorización explícita antes de probar en cualquier sistema. El uso no autorizado es ilegal.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para añadir nuevos módulos o mejorar funcionalidades:

1. Fork el repositorio
2. Crea tu rama (`git checkout -b feature/nuevo-modulo`)
3. Commit tus cambios (`git commit -am 'Añadir nuevo módulo'`)
4. Push a la rama (`git push origin feature/nuevo-modulo`)
5. Abre un Pull Request

---


## 👨‍💻 Desarrollador

**@izanasecas** — [GitHub](https://github.com/izanasecas)

---

## 🙏 Agradecimientos

Inspirado en herramientas de pentesting open-source como:

- Nmap
- Burp Suite
- Recon-ng

---

⭐ ¡Si te gusta el proyecto, dale una estrella en GitHub! ⭐
