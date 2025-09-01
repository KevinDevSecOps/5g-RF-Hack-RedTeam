def update_stats(self):
        """Actualizar estadísticas (simulado)"""
        # En producción, estos vendrían de monitoreo real
        self.dashboard_stats["threats_detected"] += 1
        self.dashboard_stats["packets_captured"] += 100
        self.dashboard_stats["signal_strength"] = -65 + (datetime.now().second % 10) - 5
        self.dashboard_stats["cpu_usage"] = 20 + (datetime.now().second % 30)
        self.dashboard_stats["memory_usage"] = 40 + (datetime.now().minute % 20)

    def start_background_tasks(self):
        """Iniciar tareas en segundo plano"""
        def stats_updater():
            while True:
                self.update_stats()
                time.sleep(5)
        
        # Iniciar hilo para actualizar stats
        thread = threading.Thread(target=stats_updater, daemon=True)
        thread.start()
        self.logger.info("Background stats updater started")

    def run(self):
        """Ejecutar servidor Flask"""
        self.start_background_tasks()
        self.app.run(
            host=self.host, 
            port=self.port, 
            debug=False,
            threaded=True
        )
    
    def run_async(self):
        """Ejecutar en segundo plano"""
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
        self.logger.info(f"Dashboard ejecutándose en http://{self.host}:{self.port}")

# Singleton instance
dashboard_instance = None

def get_dashboard_instance(host='0.0.0.0', port=5000):
    """Obtener instancia singleton del dashboard"""
    global dashboard_instance
    if dashboard_instance is None:
        dashboard_instance = Dashboard(host, port)
    return dashboard_instance