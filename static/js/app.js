/*
JavaScript untuk Temperature Converter
File ini berisi semua fungsi JavaScript untuk interaksi user
Termasuk AJAX, validasi, dan utility functions
*/

// Object utama untuk menampung semua fungsi aplikasi
const TemperatureApp = {
    // Konfigurasi aplikasi
    config: {
        apiEndpoint: '/convert',
        debounceDelay: 300,
        animationDuration: 300
    },
    
    // Fungsi-fungsi utility
    utils: {
        // Debounce untuk mengurangi request berlebihan
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Format angka sesuai locale Indonesia
        formatNumber: function(num, decimals = 2) {
            return parseFloat(num).toLocaleString('id-ID', {
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            });
        },
        
        // Validasi input temperatur
        isValidTemperature: function(value) {
            const num = parseFloat(value);
            return !isNaN(num) && isFinite(num);
        },
        
        // Ambil unit temperatur dari jenis konversi
        getTemperatureUnit: function(conversionType) {
            const unitMap = {
                'Celcius ke Fahrenheit': { from: '°C', to: '°F' },
                'Celcius ke Kelvin': { from: '°C', to: 'K' },
                'Celcius ke Reamur': { from: '°C', to: '°Re' },
                'Fahrenheit ke Celcius': { from: '°F', to: '°C' },
                'Kelvin ke Celcius': { from: 'K', to: '°C' },
                'Reamur ke Celcius': { from: '°Re', to: '°C' }
            };
            return unitMap[conversionType] || { from: '', to: '' };
        }
    },
    
    // Fungsi untuk menyimpan data di browser
    storage: {
        // Simpan riwayat konversi
        saveHistory: function(conversion) {
            try {
                let history = JSON.parse(localStorage.getItem('temperatureHistory') || '[]');
                history.unshift({
                    ...conversion,
                    timestamp: new Date().toISOString()
                });
                // Simpan hanya 10 konversi terakhir
                history = history.slice(0, 10);
                localStorage.setItem('temperatureHistory', JSON.stringify(history));
            } catch (error) {
                console.warn('Failed to save to localStorage:', error);
            }
        },
        
        // Ambil riwayat konversi
        getHistory: function() {
            try {
                return JSON.parse(localStorage.getItem('temperatureHistory') || '[]');
            } catch (error) {
                console.warn('Failed to read from localStorage:', error);
                return [];
            }
        },
        
        // Hapus riwayat
        clearHistory: function() {
            try {
                localStorage.removeItem('temperatureHistory');
            } catch (error) {
                console.warn('Failed to clear localStorage:', error);
            }
        }
    },
    
    // Fungsi untuk tracking (sederhana)
    analytics: {
        // Track event konversi
        trackConversion: function(conversionType, inputValue, result) {
            // Tracking sederhana ke console
            console.log('Conversion tracked:', {
                type: conversionType,
                input: inputValue,
                result: result,
                timestamp: new Date().toISOString()
            });
        },
        
        // Track event error
        trackError: function(error, context) {
            console.error('Error tracked:', {
                error: error,
                context: context,
                timestamp: new Date().toISOString()
            });
        }
    },
    
    // Sistem notifikasi toast
    notification: {
        // Tampilkan notifikasi toast
        showToast: function(message, type = 'info', duration = 3000) {
            // Buat element toast
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = `
                <div class="toast-body">
                    <i class="fas fa-${this.getIcon(type)} me-2"></i>
                    ${message}
                </div>
            `;
            
            // Tambahkan ke DOM
            document.body.appendChild(toast);
            
            // Hapus otomatis setelah durasi tertentu
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, duration);
        },
        
        // Ambil icon sesuai tipe toast
        getIcon: function(type) {
            const icons = {
                'success': 'check-circle',
                'error': 'exclamation-circle',
                'warning': 'exclamation-triangle',
                'info': 'info-circle'
            };
            return icons[type] || 'info-circle';
        }
    },
    
    // Shortcut keyboard
    keyboard: {
        // Inisialisasi shortcut keyboard
        init: function() {
            document.addEventListener('keydown', (e) => {
                // Ctrl + Enter: Submit form
                if (e.ctrlKey && e.key === 'Enter') {
                    e.preventDefault();
                    const form = document.getElementById('temperatureForm');
                    if (form) form.dispatchEvent(new Event('submit'));
                }
                
                // Escape: Bersihkan form
                if (e.key === 'Escape') {
                    if (typeof window.clearForm === 'function') {
                        window.clearForm();
                    }
                }
                
                // Ctrl + I: Tampilkan info
                if (e.ctrlKey && e.key === 'i') {
                    e.preventDefault();
                    if (typeof window.showInfo === 'function') {
                        window.showInfo();
                    }
                }
            });
        }
    },
    
    // Inisialisasi aplikasi
    init: function() {
        console.log('🌡️ Temperature Converter App Utils initialized');
        this.keyboard.init();
        
        // Info versi di console
        console.log('%c🚀 Temperature Converter v1.0', 'color: #4CAF50; font-weight: bold;');
        console.log('%cShortcut keyboard:', 'color: #666; font-weight: bold;');
        console.log('  Ctrl + Enter: Convert');
        console.log('  Escape: Bersihkan form');
        console.log('  Ctrl + I: Tampilkan info');
    }
};

// Inisialisasi ketika DOM sudah loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => TemperatureApp.init());
} else {
    TemperatureApp.init();
}

// Export untuk penggunaan global
window.TemperatureApp = TemperatureApp;