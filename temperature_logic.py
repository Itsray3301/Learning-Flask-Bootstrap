"""
Logic Konversi Temperatur
File ini berisi semua fungsi untuk konversi antar unit temperatur
Dipisah dari app.py agar kode lebih rapi dan mudah di-maintain
"""

from typing import Dict, Tuple

# Konstanta untuk perhitungan konversi
KELVIN_OFFSET = 273.15
FAHRENHEIT_MULTIPLIER = 9/5
FAHRENHEIT_OFFSET = 32
REAMUR_MULTIPLIER = 4/5

# Daftar opsi konversi yang tersedia
CONVERSION_OPTIONS = [
    "Celcius ke Fahrenheit",
    "Celcius ke Kelvin", 
    "Celcius ke Reamur",
    "Fahrenheit ke Celcius",
    "Kelvin ke Celcius",
    "Reamur ke Celcius"
]

class TemperatureConverter:
    """
    Class untuk menangani semua konversi temperatur
    Setiap method menangani satu jenis konversi
    """
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Konversi dari Celsius ke Fahrenheit: °F = (°C × 9/5) + 32"""
        return celsius * FAHRENHEIT_MULTIPLIER + FAHRENHEIT_OFFSET
    
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Konversi dari Celsius ke Kelvin: K = °C + 273.15"""
        return celsius + KELVIN_OFFSET
    
    @staticmethod
    def celsius_to_reamur(celsius: float) -> float:
        """Konversi dari Celsius ke Reamur: °Re = °C × 4/5"""
        return celsius * REAMUR_MULTIPLIER
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Konversi dari Fahrenheit ke Celsius: °C = (°F - 32) × 5/9"""
        return (fahrenheit - FAHRENHEIT_OFFSET) / FAHRENHEIT_MULTIPLIER
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Konversi dari Kelvin ke Celsius: °C = K - 273.15"""
        return kelvin - KELVIN_OFFSET
    
    @staticmethod
    def reamur_to_celsius(reamur: float) -> float:
        """Konversi dari Reamur ke Celsius: °C = °Re × 5/4"""
        return reamur / REAMUR_MULTIPLIER
    
    @classmethod
    def get_conversion_methods(cls) -> Dict[str, callable]:
        """Mengembalikan dictionary yang memetakan nama konversi ke method-nya"""
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
        Fungsi utama untuk konversi temperatur
        Input: nilai temperatur dan jenis konversi
        Output: (hasil_konversi, string_terformat)
        """
        conversion_methods = cls.get_conversion_methods()
        
        if conversion_type not in conversion_methods:
            raise ValueError(f"Conversion type '{conversion_type}' not supported")
        
        result = conversion_methods[conversion_type](temperature)
        formatted_result = cls._format_result(temperature, result, conversion_type)
        
        return result, formatted_result
    
    @staticmethod
    def _format_result(input_temp: float, result: float, conversion_type: str) -> str:
        """Format hasil konversi untuk ditampilkan ke user"""
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
    """Class untuk validasi input dari user"""
    
    @staticmethod
    def validate_temperature_input(input_text: str) -> Tuple[bool, float, str]:
        """
        Validasi input temperatur dari user
        Return: (valid_atau_tidak, nilai_temperatur, pesan_error)
        """
        if not input_text.strip():
            return False, 0.0, "Masukkan nilai temperatur"
        
        try:
            temperature = float(input_text)
            return True, temperature, ""
        except ValueError:
            return False, 0.0, "Masukkan angka yang valid"
