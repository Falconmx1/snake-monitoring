#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interfaz de usuario en terminal usando curses
"""

import sys
import time
import curses
from datetime import datetime
from .core import SnakeMonitor

class TerminalUI:
    """Clase que maneja la interfaz de usuario TUI"""
    
    def __init__(self, monitor):
        self.monitor = monitor
        self.screen = None
        self.running = False
        
        # Colores
        self.colors = {
            'header': 1,
            'cpu': 2,
            'ram': 3,
            'disk': 4,
            'alert': 5,
            'normal': 6
        }
    
    def _init_colors(self):
        """Inicializa los colores de curses"""
        curses.start_color()
        curses.use_default_colors()
        
        # Definir pares de colores
        curses.init_pair(1, curses.COLOR_CYAN, -1)    # Header
        curses.init_pair(2, curses.COLOR_GREEN, -1)   # CPU
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # RAM
        curses.init_pair(4, curses.COLOR_BLUE, -1)    # DISK
        curses.init_pair(5, curses.COLOR_RED, -1)     # Alert
        curses.init_pair(6, curses.COLOR_WHITE, -1)   # Normal
    
    def _draw_header(self):
        """Dibuja el encabezado"""
        h, w = self.screen.getmaxyx()
        
        # Título
        title = " 🐍 SNAKE MONITORING v1.0 "
        self.screen.attron(curses.color_pair(self.colors['header']))
        self.screen.addstr(0, 0, "╔" + "═" * (w-2) + "╗")
        self.screen.addstr(1, 0, "║")
        self.screen.addstr(1, 2, title.center(w-4))
        self.screen.addstr(1, w-1, "║")
        self.screen.addstr(2, 0, "╚" + "═" * (w-2) + "╝")
        self.screen.attroff(curses.color_pair(self.colors['header']))
        
        # Fecha y hora
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.screen.addstr(1, w - len(now) - 4, f"[ {now} ]")
    
    def _draw_bar(self, y, x, label, value, max_width, color):
        """Dibuja una barra de progreso"""
        filled = int((value / 100) * max_width)
        bar = "█" * filled + "░" * (max_width - filled)
        
        self.screen.attron(curses.color_pair(color))
        self.screen.addstr(y, x, f"{label}: ")
        self.screen.addstr(y, x + len(label) + 2, bar)
        self.screen.addstr(y, x + len(label) + 2 + max_width + 1, f"{value:5.1f}%")
        self.screen.attroff(curses.color_pair(color))
    
    def _draw_metrics(self):
        """Dibuja las métricas principales"""
        data = self.monitor.get_data()
        h, w = self.screen.getmaxyx()
        
        # Posicionar
        start_y = 4
        bar_width = min(40, w - 30)
        
        # CPU
        self._draw_bar(start_y, 2, "CPU", data['cpu'], bar_width, self.colors['cpu'])
        
        # RAM
        self._draw_bar(start_y + 1, 2, "RAM", data['ram'], bar_width, self.colors['ram'])
        
        # Disco
        self._draw_bar(start_y + 2, 2, "DISK", data['disk'], bar_width, self.colors['disk'])
        
        # Red
        net_sent = data.get('net_sent', 0) / 1024 / 1024  # MB/s
        net_recv = data.get('net_recv', 0) / 1024 / 1024  # MB/s
        self.screen.addstr(start_y + 3, 2, f"NET:  ⬆ {net_sent:.2f} MB/s  ⬇ {net_recv:.2f} MB/s")
        
        # Procesos
        self.screen.addstr(start_y + 5, 2, "📋 TOP PROCESOS:")
        processes = data.get('processes', [])[:5]
        for i, proc in enumerate(processes):
            if i >= 5:
                break
            self.screen.addstr(
                start_y + 6 + i, 4,
                f"{i+1}. {proc['name'][:15]:15} CPU: {proc['cpu']:5.1f}%  MEM: {proc['memory']:5.1f}%"
            )
    
    def _draw_history(self):
        """Dibuja un mini gráfico de historial"""
        h, w = self.screen.getmaxyx()
        history = self.monitor.get_history()
        
        start_x = w - 30
        start_y = 4
        
        self.screen.addstr(start_y, start_x, "📈 HISTORIAL")
        
        for i, key in enumerate(['cpu', 'ram', 'disk']):
            values = history[key]
            if not values:
                continue
            
            y = start_y + 1 + i
            
            # Mostrar últimos 20 valores como gráfico de barras simple
            display_values = values[-20:]
            max_val = max(display_values) if display_values else 1
            
            for j, val in enumerate(display_values):
                bar_height = int((val / max_val) * 4) if max_val > 0 else 0
                char = "█" if bar_height > 0 else "░"
                color = self.colors[key]
                
                # Usar diferentes colores según el valor
                if val > 80:
                    color = self.colors['alert']
                elif val > 60:
                    color = self.colors['cpu'] if key == 'cpu' else color
                
                self.screen.attron(curses.color_pair(color))
                self.screen.addch(y, start_x + 2 + j, char)
                self.screen.attroff(curses.color_pair(color))
    
    def _draw_footer(self):
        """Dibuja el footer con controles"""
        h, w = self.screen.getmaxyx()
        
        footer = " [q] Salir  [r] Reiniciar  [h] Ayuda "
        self.screen.attron(curses.color_pair(self.colors['normal']) | curses.A_DIM)
        self.screen.addstr(h-1, 2, footer)
        
        # Estado
        status = "🐍 Monitoreando..."
        self.screen.addstr(h-1, w - len(status) - 2, status)
        self.screen.attroff(curses.color_pair(self.colors['normal']) | curses.A_DIM)
    
    def _handle_input(self):
        """Maneja la entrada del teclado"""
        key = self.screen.getch()
        
        if key == ord('q') or key == ord('Q'):
            self.running = False
        elif key == ord('r') or key == ord('R'):
            self.monitor.stop()
            self.monitor.start()
        elif key == ord('h') or key == ord('H'):
            self._show_help()
    
    def _show_help(self):
        """Muestra la ayuda"""
        h, w = self.screen.getmaxyx()
        help_text = [
            "🐍 SNAKE MONITORING - AYUDA",
            "",
            "Atajos de teclado:",
            "  q    - Salir",
            "  r    - Reiniciar monitoreo",
            "  h    - Mostrar esta ayuda",
            "",
            "Configuración:",
            f"  CPU Threshold: {self.monitor.cpu_threshold}%",
            f"  RAM Threshold: {self.monitor.ram_threshold}%",
            f"  DISK Threshold: {self.monitor.disk_threshold}%",
            "",
            "Presiona cualquier tecla para continuar..."
        ]
        
        # Crear una ventana de ayuda
        help_win = curses.newwin(len(help_text) + 4, w - 4, 2, 2)
        help_win.box()
        
        for i, line in enumerate(help_text):
            help_win.addstr(i + 2, 3, line[:w-10])
        
        help_win.refresh()
        help_win.getch()
        help_win.clear()
    
    def run(self):
        """Ejecuta la interfaz de usuario"""
        try:
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            self.screen.keypad(True)
            self.screen.timeout(100)  # 100ms
            
            self._init_colors()
            
            # Iniciar monitor
            self.monitor.start()
            self.running = True
            
            # Bucle principal
            while self.running:
                try:
                    self.screen.clear()
                    
                    # Dibujar todo
                    self._draw_header()
                    self._draw_metrics()
                    self._draw_history()
                    self._draw_footer()
                    
                    self.screen.refresh()
                    
                    # Manejar entrada
                    self._handle_input()
                    
                except curses.error:
                    # Ignorar errores de curses (por redimensionamiento)
                    pass
                
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            pass
        finally:
            # Limpiar
            self.monitor.stop()
            if self.screen:
                curses.nocbreak()
                self.screen.keypad(False)
                curses.echo()
                curses.endwin()
            print("👋 ¡Hasta luego!")
