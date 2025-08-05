"""
Temperature Conversion Logic
Extracted from Temperature_Enhanced_UI.py untuk digunakan di web version
"""

from typing import Dict, Tuple

# Constants - Semua nilai konstan di satu tempat
KELVIN_OFFSET = 273.15
FAHRENHEIT_MULTIPLIER = 9/5
FAHRENHEIT_OFFSET = 32
REAMUR_MULTIPLIER = 4/5

# Conversion options dengan format yang konsisten
CONVERSION_OPTIONS = [
    "Celcius ke Fahrenheit",
    "Celcius ke Kelvin", 
    "Celcius ke Reamur",
    "Fahrenheit ke Celcius",
    "Kelvin ke Celcius",
    "Reamur ke Celcius"
]

class TemperatureConverter:
    """Class untuk handle semua logic konversi temperatur"""
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Konversi Celsius ke Fahrenheit"""
        return celsius * FAHRENHEIT_MULTIPLIER + FAHRENHEIT_OFFSET
    
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Konversi Celsius ke Kelvin"""
        return celsius + KELVIN_OFFSET
    
    @staticmethod
    def celsius_to_reamur(celsius: float) -> float:
        """Konversi Celsius ke Reamur"""
        return celsius * REAMUR_MULTIPLIER
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Konversi Fahrenheit ke Celsius"""
        return (fahrenheit - FAHRENHEIT_OFFSET) / FAHRENHEIT_MULTIPLIER
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Konversi Kelvin ke Celsius"""
        return kelvin - KELVIN_OFFSET
    
    @staticmethod
    def reamur_to_celsius(reamur: float) -> float:
        """Konversi Reamur ke Celsius"""
        return reamur / REAMUR_MULTIPLIER
    
    @classmethod
    def get_conversion_methods(cls) -> Dict[str, callable]:
        """Return dictionary mapping conversion names to methods"""
        return {
            "Celcius ke Fahrenheit": cls.celsius_to_fahrenheit,
            "Celcius ke Kelvin": cls.celsius_to_kelvin,
            "Celcius ke Reamur": cls.celsius_to_reamur,
            "Fahrenheit ke Celcius": cls.fahrenheit_to_celsius,
            "Kelvin ke Celcius": cls.kelvin_to_celsius,
            "Reamur ke Celcius": cls.reamur_to_celsius
        }
    
    @classmethod
    def convert(cls, temperature: float, conversion_type: str) -> Tuple[float, str]:
        """
        Convert temperature based on conversion type
        Returns: (result, formatted_string)
        """
        conversion_methods = cls.get_conversion_methods()
        
        if conversion_type not in conversion_methods:
            raise ValueError(f"Conversion type '{conversion_type}' not supported")
        
        result = conversion_methods[conversion_type](temperature)
        formatted_result = cls._format_result(temperature, result, conversion_type)
        
        return result, formatted_result
    
    @staticmethod
    def _format_result(input_temp: float, result: float, conversion_type: str) -> str:
        """Format the conversion result for display"""
        unit_mapping = {
            "Celcius ke Fahrenheit": (f"{input_temp}°C", f"{result:.2f}°F"),
            "Celcius ke Kelvin": (f"{input_temp}°C", f"{result:.2f} K"),
            "Celcius ke Reamur": (f"{input_temp}°C", f"{result:.2f}°Re"),
            "Fahrenheit ke Celcius": (f"{input_temp}°F", f"{result:.2f}°C"),
            "Kelvin ke Celcius": (f"{input_temp} K", f"{result:.2f}°C"),
            "Reamur ke Celcius": (f"{input_temp}°Re", f"{result:.2f}°C")
        }
        
        input_str, result_str = unit_mapping[conversion_type]
        return f"{input_str} = {result_str}"

class InputValidator:
    """Class untuk handle validasi input"""
    
    @staticmethod
    def validate_temperature_input(input_text: str) -> Tuple[bool, float, str]:
        """
        Validate temperature input
        Returns: (is_valid, temperature_value, error_message)
        """
        if not input_text.strip():
            return False, 0.0, "Masukkan nilai temperatur"
        
        try:
            temperature = float(input_text)
            return True, temperature, ""
        except ValueError:
            return False, 0.0, "Masukkan angka yang valid"
