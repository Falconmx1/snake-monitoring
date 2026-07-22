#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de alertas para Snake Monitoring
"""

import os
import platform
import subprocess
import logging

class AlertSystem:
    """Sistema de notificaciones y alertas"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.enabled = self.config.get('alerts_enabled', True)
        
    def send_alert(self, message, level='warning'):
        """Envía una alerta usando diferentes métodos"""
        if not self.enabled:
            return
        
        self.logger.warning(f"ALERTA [{level}]: {message}")
        
        # Enviar notificación según el sistema
        system = platform.system()
        
        if system == 'Linux':
            self._linux_notification(message)
        elif system == 'Windows':
            self._windows_notification(message)
        elif system == 'Darwin':  # macOS
            self._macos_notification(message)
    
    def _linux_notification(self, message):
        """Notificación en Linux (usando notify-send)"""
        try:
            subprocess.run([
                'notify-send',
                '🐍 Snake Monitoring',
                message,
                '--icon=dialog-warning'
            ], check=False, timeout=2)
        except:
            pass
    
    def _windows_notification(self, message):
        """Notificación en Windows"""
        try:
            # Usar PowerShell para mostrar notificación
            ps_script = f'''
            [System.Windows.Forms.MessageBox]::Show(
                '{message}',
                '🐍 Snake Monitoring',
                'OK',
                'Warning'
            )
            '''
            subprocess.run([
                'powershell', '-Command', ps_script
            ], check=False, timeout=5)
        except:
            pass
    
    def _macos_notification(self, message):
        """Notificación en macOS"""
        try:
            subprocess.run([
                'osascript',
                '-e', f'display notification "{message}" with title "🐍 Snake Monitoring"'
            ], check=False, timeout=2)
        except:
            pass
    
    def send_email_alert(self, subject, body, to_email):
        """Envía alerta por correo (placeholder)"""
        # Implementar con SMTP si se desea
        self.logger.info(f"Email alert to {to_email}: {subject} - {body}")
