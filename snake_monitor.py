#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐍 Snake Monitoring - Main entry point
Monitor de sistema en tiempo real con interfaz TUI
"""

import sys
import argparse
import json
from src.core import SnakeMonitor
from src.ui import TerminalUI

__version__ = "1.0.0"
__author__ = "Falconmx1"

def load_config(config_file="config.json"):
    """Carga la configuración desde archivo JSON"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "refresh_interval": 1.0,
            "cpu_threshold": 80,
            "ram_threshold": 90,
            "disk_threshold": 85,
            "alerts_enabled": True,
            "theme": "default"
        }
    except json.JSONDecodeError:
        print("⚠️ Error: config.json tiene formato inválido. Usando defaults.")
        return {}

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="🐍 Snake Monitoring - Monitor de sistema en tiempo real"
    )
    parser.add_argument(
        "--config", 
        default="config.json",
        help="Archivo de configuración (JSON)"
    )
    parser.add_argument(
        "--version", 
        action="version",
        version=f"Snake Monitoring v{__version__}"
    )
    parser.add_argument(
        "--no-alerts",
        action="store_true",
        help="Desactivar alertas"
    )
    
    args = parser.parse_args()
    
    # Cargar configuración
    config = load_config(args.config)
    if args.no_alerts:
        config["alerts_enabled"] = False
    
    # Inicializar monitor
    monitor = SnakeMonitor(config)
    
    # Inicializar UI
    ui = TerminalUI(monitor)
    
    # Ejecutar
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)

if __name__ == "__main__":
    main()
