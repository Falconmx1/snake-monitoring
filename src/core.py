#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Núcleo del monitor: recolección y procesamiento de métricas
"""

import psutil
import time
import logging
from datetime import datetime
from threading import Thread, Event

class SnakeMonitor:
    """Clase principal que maneja el monitoreo del sistema"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.refresh_interval = self.config.get("refresh_interval", 1.0)
        self.cpu_threshold = self.config.get("cpu_threshold", 80)
        self.ram_threshold = self.config.get("ram_threshold", 90)
        self.disk_threshold = self.config.get("disk_threshold", 85)
        self.alerts_enabled = self.config.get("alerts_enabled", True)
        
        self.running = False
        self.thread = None
        self.stop_event = Event()
        
        # Datos actuales
        self.current_data = {
            "cpu": 0.0,
            "ram": 0.0,
            "disk": 0.0,
            "net_sent": 0,
            "net_recv": 0,
            "processes": [],
            "timestamp": None
        }
        
        # Historial para gráficos
        self.history = {
            "cpu": [],
            "ram": [],
            "disk": []
        }
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=self.config.get("log_file", "snake_monitor.log")
        )
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Inicia el monitoreo en un hilo separado"""
        if self.running:
            return
        
        self.running = True
        self.stop_event.clear()
        self.thread = Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        self.logger.info("Monitor iniciado")
    
    def stop(self):
        """Detiene el monitoreo"""
        self.running = False
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=2)
        self.logger.info("Monitor detenido")
    
    def _monitor_loop(self):
        """Bucle principal de monitoreo"""
        last_net = psutil.net_io_counters()
        
        while self.running and not self.stop_event.is_set():
            try:
                # Obtener métricas
                cpu = psutil.cpu_percent(interval=0.1)
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                
                # Métricas de red
                net = psutil.net_io_counters()
                net_sent = net.bytes_sent - last_net.bytes_sent
                net_recv = net.bytes_recv - last_net.bytes_recv
                last_net = net
                
                # Procesos
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        pinfo = proc.info
                        processes.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'cpu': pinfo['cpu_percent'],
                            'memory': pinfo['memory_percent']
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                # Ordenar procesos por CPU
                processes.sort(key=lambda x: x['cpu'], reverse=True)
                
                # Actualizar datos
                self.current_data = {
                    "cpu": cpu,
                    "ram": ram,
                    "disk": disk,
                    "net_sent": net_sent,
                    "net_recv": net_recv,
                    "processes": processes[:10],
                    "timestamp": datetime.now()
                }
                
                # Actualizar historial
                self.history["cpu"].append(cpu)
                self.history["ram"].append(ram)
                self.history["disk"].append(disk)
                
                # Mantener historial limitado
                max_history = 60
                for key in self.history:
                    if len(self.history[key]) > max_history:
                        self.history[key].pop(0)
                
                # Verificar alertas
                if self.alerts_enabled:
                    self._check_alerts()
                
                time.sleep(self.refresh_interval)
                
            except Exception as e:
                self.logger.error(f"Error en monitoreo: {e}")
                time.sleep(1)
    
    def _check_alerts(self):
        """Verifica umbrales y genera alertas"""
        alerts = []
        
        if self.current_data["cpu"] > self.cpu_threshold:
            alerts.append(f"⚠️ CPU al {self.current_data['cpu']:.1f}% (umbral: {self.cpu_threshold}%)")
        
        if self.current_data["ram"] > self.ram_threshold:
            alerts.append(f"⚠️ RAM al {self.current_data['ram']:.1f}% (umbral: {self.ram_threshold}%)")
        
        if self.current_data["disk"] > self.disk_threshold:
            alerts.append(f"⚠️ Disco al {self.current_data['disk']:.1f}% (umbral: {self.disk_threshold}%)")
        
        if alerts:
            self.logger.warning("Alertas: " + " | ".join(alerts))
            # Aquí se podrían enviar notificaciones adicionales
        
        return alerts
    
    def get_data(self):
        """Retorna los datos actuales del sistema"""
        return self.current_data
    
    def get_history(self):
        """Retorna el historial de métricas"""
        return self.history
