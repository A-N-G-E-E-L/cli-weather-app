#!/usr/bin/env python3
"""
🌤️ CLI Weather App con Open-Meteo
Consulta el clima actual de una ciudad desde la terminal.
No requiere API key.
"""

import sys
import argparse
import requests

def get_coordinates(city: str) -> tuple:
    """
    Busca las coordenadas (latitud, longitud) de una ciudad
    usando la API de geocodificación de Open-Meteo.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,          # Solo el primer resultado
        "language": "es",    # Resultados en español
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Lanza error si la petición falla
        data = response.json()
        
        if not data.get("results"):
            print(f"❌ Ciudad no encontrada: '{city}'")
            print("💡 Intenta con el nombre en inglés o añade el país. Ej: 'Madrid, Spain'")
            sys.exit(1)
        
        result = data["results"][0]
        return result["latitude"], result["longitude"], result["name"], result["country"]
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión al buscar coordenadas: {e}")
        sys.exit(1)


def get_weather(lat: float, lon: float) -> dict:
    """
    Obtiene el clima actual usando las coordenadas.
    API: https://open-meteo.com/
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,weather_code,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto",  # Usa la zona horaria de las coordenadas
        "forecast_days": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión al obtener el clima: {e}")
        sys.exit(1)


def get_weather_description(code: int) -> str:
    """
    Convierte el código numérico del clima a texto en español.
    Basado en: https://open-meteo.com/en/docs
    """
    descriptions = {
        0: "Cielo despejado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna densa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia fuerte",
        71: "Nieve ligera",
        73: "Nieve moderada",
        75: "Nieve fuerte",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos violentos",
        95: "Tormenta eléctrica",
        96: "Tormenta con granizo ligero",
        99: "Tormenta con granizo fuerte",
    }
    return descriptions.get(code, "Condiciones desconocidas")


def display_weather(city: str, country: str, current: dict) -> None:
    """Muestra el clima formateado en la terminal."""
    temp = current["temperature_2m"]
    feels_like = current["apparent_temperature"]
    code = current["weather_code"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]
    description = get_weather_description(code)

    print(f"\n🌤️  Clima en {city}, {country}")
    print(f"🌡️  Temperatura: {temp}°C (Sensación: {feels_like}°C)")
    print(f"☁️  Descripción: {description}")
    print(f"💧 Humedad: {humidity}%")
    print(f"💨 Viento: {wind} km/h\n")


def main() -> None:
    """Función principal: parsea argumentos y ejecuta el flujo."""
    parser = argparse.ArgumentParser(
        description="🌤️ Consulta el clima actual desde la terminal (sin API key)."
    )
    parser.add_argument(
        "city",
        help="Nombre de la ciudad (ej: 'Madrid', 'Bogota', 'Buenos Aires')"
    )
    args = parser.parse_args()

    print(f"🔍 Buscando '{args.city}'...")
    
    # Paso 1: Obtener coordenadas
    lat, lon, city_name, country = get_coordinates(args.city)
    
    # Paso 2: Obtener datos del clima
    data = get_weather(lat, lon)
    
    # Paso 3: Mostrar resultados
    display_weather(city_name, country, data["current"])


if __name__ == "__main__":
    main()