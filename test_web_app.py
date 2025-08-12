"""
Unit Test untuk Temperature Converter Web App
File ini berisi semua test case untuk memastikan aplikasi berjalan dengan baik
Menggunakan unittest framework bawaan Python
"""

import unittest
import json
import sys
import os

# Tambahkan directory parent untuk import module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from temperature_logic import TemperatureConverter, InputValidator

class TestTemperatureWebApp(unittest.TestCase):
    """Test case untuk aplikasi Flask"""
    
    def setUp(self):
        """Setup environment untuk testing"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_homepage(self):
        """Test apakah homepage bisa diakses"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Konversi Temperatur', response.data)
        self.assertIn(b'Masukkan Temperatur', response.data)
    
    def test_convert_api_success(self):
        """Test konversi yang berhasil via API"""
        data = {
            'temperature': '25',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        json_data = json.loads(response.data)
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['result'], 77.0)
        self.assertEqual(json_data['formatted_result'], '25.0°C = 77.00°F')
    
    def test_convert_api_invalid_input(self):
        """Test API dengan input yang tidak valid"""
        data = {
            'temperature': 'invalid',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        json_data = json.loads(response.data)
        self.assertFalse(json_data['success'])
        self.assertIn('error', json_data)
    
    def test_convert_api_empty_input(self):
        """Test API dengan input kosong"""
        data = {
            'temperature': '',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        json_data = json.loads(response.data)
        self.assertFalse(json_data['success'])
        self.assertEqual(json_data['error'], 'Masukkan nilai temperatur')
    
    def test_convert_api_invalid_conversion_type(self):
        """Test API dengan tipe konversi yang tidak valid"""
        data = {
            'temperature': '25',
            'conversion_type': 'Invalid Conversion'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        json_data = json.loads(response.data)
        self.assertFalse(json_data['success'])
        self.assertIn('not supported', json_data['error'])
    
    def test_conversions_api(self):
        """Test API untuk mendapatkan opsi konversi"""
        response = self.app.get('/api/conversions')
        self.assertEqual(response.status_code, 200)
        
        json_data = json.loads(response.data)
        self.assertIsInstance(json_data, list)
        self.assertIn('Celcius ke Fahrenheit', json_data)
        self.assertIn('Fahrenheit ke Celcius', json_data)
    
    def test_health_check(self):
        """Test endpoint health check"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        json_data = json.loads(response.data)
        self.assertEqual(json_data['status'], 'healthy')
        self.assertEqual(json_data['service'], 'Temperature Converter API')
    
    def test_404_error(self):
        """Test handling error 404"""
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
    
    def test_json_404_error(self):
        """Test error 404 untuk request API"""
        response = self.app.get('/api/nonexistent',
                               headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 404)
        
        json_data = json.loads(response.data)
        self.assertEqual(json_data['error'], 'Endpoint not found')

class TestTemperatureLogicReuse(unittest.TestCase):
    """Test logic konversi temperatur"""
    
    def test_temperature_converter_methods(self):
        """Test semua fungsi konversi temperatur"""
        # Test Celsius conversions
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(0), 32.0)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(100), 212.0)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_reamur(100), 80.0)
        
        # Test reverse conversions
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(212), 100.0)
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(273.15), 0.0)
        self.assertAlmostEqual(TemperatureConverter.reamur_to_celsius(80), 100.0)
    
    def test_input_validator(self):
        """Test validasi input"""
        # Input yang valid
        valid, value, msg = InputValidator.validate_temperature_input("25")
        self.assertTrue(valid)
        self.assertEqual(value, 25.0)
        self.assertEqual(msg, "")
        
        # Input yang tidak valid
        valid, value, msg = InputValidator.validate_temperature_input("")
        self.assertFalse(valid)
        self.assertEqual(msg, "Masukkan nilai temperatur")
        
        valid, value, msg = InputValidator.validate_temperature_input("abc")
        self.assertFalse(valid)
        self.assertEqual(msg, "Masukkan angka yang valid")
    
    def test_conversion_integration(self):
        """Test proses konversi secara keseluruhan"""
        result, formatted = TemperatureConverter.convert(0, "Celcius ke Fahrenheit")
        self.assertEqual(result, 32.0)
        self.assertEqual(formatted, "0°C = 32.00°F")
        
        result, formatted = TemperatureConverter.convert(100, "Celcius ke Kelvin")
        self.assertEqual(result, 373.15)
        self.assertEqual(formatted, "100°C = 373.15 K")

class TestAPIValidation(unittest.TestCase):
    """Test validasi API dan kasus-kasus khusus"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_extreme_temperatures(self):
        """Test dengan temperatur yang ekstrem"""
        # Test absolute zero
        data = {
            'temperature': '-273.15',
            'conversion_type': 'Celcius ke Kelvin'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        json_data = json.loads(response.data)
        self.assertTrue(json_data['success'])
        self.assertAlmostEqual(json_data['result'], 0.0)
    
    def test_large_numbers(self):
        """Test dengan angka yang sangat besar"""
        data = {
            'temperature': '1000000',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        json_data = json.loads(response.data)
        self.assertTrue(json_data['success'])
        self.assertIsInstance(json_data['result'], (int, float))
    
    def test_decimal_precision(self):
        """Test presisi dengan angka desimal"""
        data = {
            'temperature': '25.6789',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        json_data = json.loads(response.data)
        self.assertTrue(json_data['success'])
        # Cek apakah hasil tetap presisi
        expected = 25.6789 * 9/5 + 32
        self.assertAlmostEqual(json_data['result'], expected, places=4)

if __name__ == '__main__':
    # Jalankan test dengan output yang detail
    unittest.main(verbosity=2)
