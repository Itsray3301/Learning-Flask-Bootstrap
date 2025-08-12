// Test untuk Temperature Converter
// Unit test sederhana untuk fungsi konversi suhu

// Fungsi konversi (copy dari server.js untuk testing)
function celsiusToFahrenheit(celsius) {
  return (celsius * 9/5) + 32;
}

function fahrenheitToCelsius(fahrenheit) {
  return (fahrenheit - 32) * 5/9;
}

function celsiusToKelvin(celsius) {
  return celsius + 273.15;
}

function kelvinToCelsius(kelvin) {
  return kelvin - 273.15;
}

// Simple test runner
function runTests() {
  let passed = 0;
  let failed = 0;
  
  function test(description, testFunction) {
    try {
      testFunction();
      console.log(`✅ ${description}`);
      passed++;
    } catch (error) {
      console.log(`❌ ${description}: ${error.message}`);
      failed++;
    }
  }
  
  function assertEqual(actual, expected, tolerance = 0.01) {
    if (Math.abs(actual - expected) > tolerance) {
      throw new Error(`Expected ${expected}, got ${actual}`);
    }
  }
  
  console.log('🧪 Menjalankan test konversi suhu...\n');
  
  // Test Celsius ke Fahrenheit
  test('Celsius ke Fahrenheit: 0°C = 32°F', () => {
    assertEqual(celsiusToFahrenheit(0), 32);
  });
  
  test('Celsius ke Fahrenheit: 100°C = 212°F', () => {
    assertEqual(celsiusToFahrenheit(100), 212);
  });
  
  test('Celsius ke Fahrenheit: 25°C = 77°F', () => {
    assertEqual(celsiusToFahrenheit(25), 77);
  });
  
  // Test Fahrenheit ke Celsius
  test('Fahrenheit ke Celsius: 32°F = 0°C', () => {
    assertEqual(fahrenheitToCelsius(32), 0);
  });
  
  test('Fahrenheit ke Celsius: 212°F = 100°C', () => {
    assertEqual(fahrenheitToCelsius(212), 100);
  });
  
  // Test Celsius ke Kelvin
  test('Celsius ke Kelvin: 0°C = 273.15K', () => {
    assertEqual(celsiusToKelvin(0), 273.15);
  });
  
  test('Celsius ke Kelvin: 100°C = 373.15K', () => {
    assertEqual(celsiusToKelvin(100), 373.15);
  });
  
  // Test Kelvin ke Celsius
  test('Kelvin ke Celsius: 273.15K = 0°C', () => {
    assertEqual(kelvinToCelsius(273.15), 0);
  });
  
  test('Kelvin ke Celsius: 373.15K = 100°C', () => {
    assertEqual(kelvinToCelsius(373.15), 100);
  });
  
  // Test edge cases
  test('Celsius ke Fahrenheit: -40°C = -40°F', () => {
    assertEqual(celsiusToFahrenheit(-40), -40);
  });
  
  console.log(`\n📊 Hasil Test:`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📈 Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);
  
  if (failed === 0) {
    console.log('\n🎉 Semua test berhasil!');
  } else {
    console.log('\n⚠️ Ada test yang gagal. Periksa kode!');
  }
}

// Jalankan test
runTests();