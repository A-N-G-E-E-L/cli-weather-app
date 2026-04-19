"""
Tests para CLI Weather App.
Validan que las funciones principales devuelvan lo esperado sin hacer llamadas reales a internet.
"""

import pytest # type: ignore
from unittest.mock import patch, MagicMock
from weather import get_weather_description, get_coordinates

# 1️⃣ Test puro: mapeo de código climático a texto
def test_weather_description_known_codes():
    assert get_weather_description(0) == "Cielo despejado"
    assert get_weather_description(61) == "Lluvia ligera"
    assert get_weather_description(95) == "Tormenta eléctrica"

def test_weather_description_unknown_code():
    assert get_weather_description(999) == "Condiciones desconocidas"

# 2️⃣ Test con mock: simulamos la respuesta de la API para no depender de internet
@patch("weather.requests.get")
def test_get_coordinates_success(mock_get):
    # Simulamos lo que devolvería Open-Meteo
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [{
            "latitude": 40.4168, 
            "longitude": -3.7038,
            "name": "Madrid", 
            "country": "Spain"
        }]
    }
    mock_get.return_value = mock_response

    # Ejecutamos la función real
    lat, lon, name, country = get_coordinates("Madrid")

    # Validamos resultados
    assert lat == 40.4168
    assert lon == -3.7038
    assert name == "Madrid"
    assert country == "Spain"
    
    # Verificamos que la petición se hizo exactamente 1 vez
    mock_get.assert_called_once()