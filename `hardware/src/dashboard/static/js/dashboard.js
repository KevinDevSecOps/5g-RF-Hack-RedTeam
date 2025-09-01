class FiveGDashboard {
    constructor() {
        this.updateIntervals = {};
        this.isConnected = true;
        this.init();
    }

    init() {
        console.log('5G RF RedTeam Dashboard initialized');
        this.setupEventListeners();
        this.startPeriodicUpdates();
        this.checkConnection();
    }

    setupEventListeners() {
        // Event listeners para botones y controles
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-scan')) {
                this.startScan();
            } else if (e.target.classList.contains('btn-stop')) {
                this.stopScan();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                this.startScan();
            } else if (e.ctrlKey && e.key === 'x') {
                e.preventDefault();
                this.stopScan();
            }
        });
    }

    async startScan() {
        try {
            const response = await fetch('/api/scan/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            this.showNotification(data.message, 'success');
            this.updateScanStatus();
            
        } catch (error) {
            console.error('Error starting scan:', error);
            this.showNotification('Error starting scan', 'danger');
        }
    }

    async stopScan() {
        try {
            const response = await fetch('/api/scan/stop', {
                method: 'POST'
            });
            
            const data = await response.json();
            this.showNotification(data.message, 'info');
            this.updateScanStatus();
            
        } catch (error) {
            console.error('Error stopping scan:', error);
            this.showNotification('Error stopping scan', 'danger');
        }
    }

    async updateDashboardStats() {
        try {
            const response = await fetch('/api/dashboard/stats');
            const data = await response.json();
            
            // Actualizar UI con los datos
            this.updateStatsDisplay(data);
            
        } catch (error) {
            console.error('Error updating stats:', error);
            this.setConnectionStatus(false);
        }
    }

    updateStatsDisplay(stats) {
        // Actualizar todos los elementos del dashboard
        const elements = {
            'signal-strength': `${stats.signal_strength} dBm`,
            'frequency': `${(stats.frequency / 1e9).toFixed(2)} GHz`,
            'threats-detected': stats.threats_detected,
            'packets-captured': stats.packets_captured.toLocaleString(),
            'cpu-usage': `${stats.cpu_usage}%`,
            'memory-usage': `${stats.memory_usage}%`
        };

        for (const [id, value] of Object.entries(elements)) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
                
                // Animación de cambio
                element.classList.add('pulse');
                setTimeout(() => element.classList.remove('pulse'), 500);
            }
        }
    }

    async updateSpectrumData() {
        try {
            const response = await fetch('/api/spectrum/data');
            const data = await response.json();
            
            this.plotSpectrum(data);
            this.updateDetectionTable(data);
            
        } catch (error) {
            console.error('Error updating spectrum data:', error);
        }
    }

    plotSpectrum(data) {
        const plotElement = document.getElementById('spectrum-plot');
        if (!plotElement) return;

        const plotData = [{
            x: data.frequencies,
            y: data.spectrum,
            type: 'line',
            line: { color: '#667eea', width: 2 },
            name: 'Spectrum'
        }];

        // Añadir marcadores para picos
        if (data.peaks && data.peaks.length > 0) {
            data.peaks.forEach(peak => {
                plotData.push({
                    x: [peak.frequency],
                    y: [peak.power],
                    mode: 'markers+text',
                    marker: { color: 'red', size: 10 },
                    text: [`${(peak.frequency/1e9).toFixed(2)}GHz`],
                    textposition: 'top',
                    name: 'Peak'
                });
            });
        }

        const layout = {
            title: '5G Spectrum Analysis',
            xaxis: { 
                title: 'Frequency (Hz)',
                tickformat: '.2s'
            },
            yaxis: { title: 'Power (dB)' },
            height: 500,
            margin: { l: 60, r: 30, t: 60, b: 60 },
            showlegend: false
        };

        Plotly.react('spectrum-plot', plotData, layout);
    }

    updateDetectionTable(data) {
        const tableBody = document.querySelector('#detections-table tbody');
        if (!tableBody) return;

        // Limpiar tabla existente
        tableBody.innerHTML = '';

        if (data.peaks && data.peaks.length > 0) {
            data.peaks.forEach(peak => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${new Date().toLocaleTimeString()}</td>
                    <td>${(peak.frequency / 1e9).toFixed(3)} GHz</td>
                    <td>${peak.power.toFixed(1)} dB</td>
                    <td>RF Signal</td>
                    <td><span class="badge bg-warning">Detected</span></td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center">No signals detected</td>
                </tr>
            `;
        }
    }

    startPeriodicUpdates() {
        // Actualizar estadísticas cada 3 segundos
        this.updateIntervals.stats = setInterval(() => {
            this.updateDashboardStats();
        }, 3000);

        // Actualizar spectrum cada 2 segundos
        this.updateIntervals.spectrum = setInterval(() => {
            this.updateSpectrumData();
        }, 2000);

        // Verificar conexión cada 10 segundos
        this.updateIntervals.connection = setInterval(() => {
            this.checkConnection();
        }, 10000);
    }

    async checkConnection() {
        try {
            const response = await fetch('/api/system/status', {
                signal: AbortSignal.timeout(5000)
            });
            
            this.setConnectionStatus(response.ok);
            
        } catch (error) {
            console.error('Connection check failed:', error);
            this.setConnectionStatus(false);
        }
    }

    setConnectionStatus(connected) {
        const statusBadge = document.getElementById('status-badge');
        if (!statusBadge) return;

        this.isConnected = connected;
        
        if (connected) {
            statusBadge.className = 'badge bg-success';
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Connected';
        } else {
            statusBadge.className = 'badge bg-danger';
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Disconnected';
        }
    }

    showNotification(message, type = 'info') {
        // Crear notificación toast de Bootstrap
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
        
        const toastId = 'toast-' + Date.now();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.id = toastId;
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        // Mostrar el toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remover después de que se oculte
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }

    emergencyStop() {
        if (confirm('Are you sure you want to emergency stop all operations?')) {
            this.stopScan();
            this.showNotification('Emergency stop activated', 'danger');
            
            // Detener todas las actualizaciones
            Object.values(this.updateIntervals).forEach(interval => {
                clearInterval(interval);
            });
        }
    }
}

// Inicializar dashboard cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.fiveGDashboard = new FiveGDashboard();
});

// Funciones globales para los botones HTML
function startScan() {
    if (window.fiveGDashboard) {
        window.fiveGDashboard.startScan();
    }
}

function stopScan() {
    if (window.fiveGDashboard) {
        window.fiveGDashboard.stopScan();
    }
}

function emergencyStop() {
    if (window.fiveGDashboard) {
        window.fiveGDashboard.emergencyStop();
    }
}

function capturePackets() {
    if (window.fiveGDashboard) {
        window.fiveGDashboard.showNotification('Packet capture started', 'info');
    }
}