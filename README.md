# 🌤️ CLI Weather App

Consulta el clima actual de cualquier ciudad directamente desde tu terminal, usando la API gratuita de Open-Meteo (sin API key).

## ✨ Características
- 🌍 Datos en tiempo real vía Open-Meteo
- 🗺️ Geocodificación automática (no necesitas coordenadas)
- 📏 Temperatura en °C, viento en km/h
- 🌐 Descripciones en español
- 🛡️ Manejo de errores claro

## 🛠️ Requisitos
- Python 3.8 o superior
- Conexión a internet

## 📦 Instalación
```bash
# Clona o crea la carpeta del proyecto
cd cli-weather-app

# Crea y activa el entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows PowerShell

# Instala dependencias
pip install -r requirements.txt