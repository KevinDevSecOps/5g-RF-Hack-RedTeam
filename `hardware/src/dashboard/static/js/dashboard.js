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

        const layout =