/*
Temperature Converter Web App - JavaScript
Author: itsray3301
*/

// Temperature Converter Web App Utils
const TemperatureApp = {
    // Configuration
    config: {
        apiEndpoint: '/convert',
        debounceDelay: 300,
        animationDuration: 300
    },
    
    // Utility functions
    utils: {
        // Debounce function for input events
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
        
        // Format number with locale
        formatNumber: function(num, decimals = 2) {
            return parseFloat(num).toLocaleString('id-ID', {
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            });
        },
        
        // Validate temperature input
        isValidTemperature: function(value) {
            const num = parseFloat(value);
            return !isNaN(num) && isFinite(num);
        },
        
        // Get temperature unit from conversion type
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
    
    // Local storage functions
    storage: {
        // Save conversion history
        saveHistory: function(conversion) {
            try {
                let history = JSON.parse(localStorage.getItem('temperatureHistory') || '[]');
                history.unshift({
                    ...conversion,
                    timestamp: new Date().toISOString()
                });
                // Keep only last 10 conversions
                history = history.slice(0, 10);
                localStorage.setItem('temperatureHistory', JSON.stringify(history));
            } catch (error) {
                console.warn('Failed to save to localStorage:', error);
            }
        },
        
        // Get conversion history
        getHistory: function() {
            try {
                return JSON.parse(localStorage.getItem('temperatureHistory') || '[]');
            } catch (error) {
                console.warn('Failed to read from localStorage:', error);
                return [];
            }
        },
        
        // Clear history
        clearHistory: function() {
            try {
                localStorage.removeItem('temperatureHistory');
            } catch (error) {
                console.warn('Failed to clear localStorage:', error);
            }
        }
    },
    
    // Analytics functions
    analytics: {
        // Track conversion event
        trackConversion: function(conversionType, inputValue, result) {
            // Simple analytics tracking
            console.log('Conversion tracked:', {
                type: conversionType,
                input: inputValue,
                result: result,
                timestamp: new Date().toISOString()
            });
        },
        
        // Track error event
        trackError: function(error, context) {
            console.error('Error tracked:', {
                error: error,
                context: context,
                timestamp: new Date().toISOString()
            });
        }
    },
    
    // Notification system
    notification: {
        // Show toast notification
        showToast: function(message, type = 'info', duration = 3000) {
            // Create toast element
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = `
                <div class="toast-body">
                    <i class="fas fa-${this.getIcon(type)} me-2"></i>
                    ${message}
                </div>
            `;
            
            // Add to DOM
            document.body.appendChild(toast);
            
            // Auto remove after duration
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, duration);
        },
        
        // Get icon for toast type
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
    
    // Keyboard shortcuts
    keyboard: {
        // Initialize keyboard shortcuts
        init: function() {
            document.addEventListener('keydown', (e) => {
                // Ctrl + Enter: Submit form
                if (e.ctrlKey && e.key === 'Enter') {
                    e.preventDefault();
                    const form = document.getElementById('temperatureForm');
                    if (form) form.dispatchEvent(new Event('submit'));
                }
                
                // Escape: Clear form
                if (e.key === 'Escape') {
                    if (typeof window.clearForm === 'function') {
                        window.clearForm();
                    }
                }
                
                // Ctrl + I: Show info
                if (e.ctrlKey && e.key === 'i') {
                    e.preventDefault();
                    if (typeof window.showInfo === 'function') {
                        window.showInfo();
                    }
                }
            });
        }
    },
    
    // Initialize the app
    init: function() {
        console.log('🌡️ Temperature Converter App Utils initialized');
        this.keyboard.init();
        
        // Add version info to console
        console.log('%c🚀 Temperature Converter v1.0', 'color: #4CAF50; font-weight: bold;');
        console.log('%cKeyboard shortcuts:', 'color: #666; font-weight: bold;');
        console.log('  Ctrl + Enter: Convert');
        console.log('  Escape: Clear form');
        console.log('  Ctrl + I: Show info');
    }
};

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => TemperatureApp.init());
} else {
    TemperatureApp.init();
}

// Export for global use
window.TemperatureApp = TemperatureApp;