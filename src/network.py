#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Funciones de red para Snake Monitoring
"""

import psutil
import socket
import subprocess
import platform

def get_network_interfaces():
    """Obtiene todas las interfaces de red activas"""
    interfaces = {}
    
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            iface_data = []
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    iface_data.append({
                        'type': 'IPv4',
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
                elif addr.family == socket.AF_INET6:
                    iface_data.append({
                        'type': 'IPv6',
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
            if iface_data:
                interfaces[iface] = iface_data
    except Exception as e:
        print(f"Error obteniendo interfaces: {e}")
    
    return interfaces

def get_network_speed(interface='eth0'):
    """Obtiene la velocidad de la interfaz"""
    try:
        # Linux
        if platform.system() == 'Linux':
            result = subprocess.run(
                ['cat', f'/sys/class/net/{interface}/speed'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
        
        # Windows
        elif platform.system() == 'Windows':
            # Usar wmic para obtener velocidad
            result = subprocess.run(
                ['wmic', 'nic', 'where', f'name="{interface}"', 'get', 'speed'],
                capture_output=True,
                text=True
            )
            # Procesar resultado...
            pass
        
        return 0
    except:
        return 0

def ping_host(host='8.8.8.8', count=4):
    """Realiza ping a un host"""
    try:
        # Diferentes parámetros según OS
        if platform.system() == 'Windows':
            cmd = ['ping', '-n', str(count), host]
        else:
            cmd = ['ping', '-c', str(count), host]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        # Procesar resultado
        if result.returncode == 0:
            # Extraer tiempos (simple)
            return {'success': True, 'output': result.stdout}
        else:
            return {'success': False, 'error': result.stderr}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}
