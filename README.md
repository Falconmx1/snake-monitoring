# 🐍 Snake Monitoring

> Monitor de sistema en tiempo real con interfaz retro estilo "snake" para terminal.  
> Compatible con Windows y Linux. Ligero, rápido y sin dependencias pesadas.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

---

## ✨ Características

- 📊 **Monitoriza en tiempo real:** CPU, RAM, Disco, Red y Procesos.
- 🎨 **Interfaz TUI:** Estilo retro con colores y animaciones (curses).
- 🔔 **Alertas:** Notificaciones cuando los recursos superan umbrales.
- 🖥️ **Multiplataforma:** Funciona en Windows y Linux.
- ⚡ **Bajo consumo:** Optimizado para servidores y equipos viejos.

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Falconmx1/snake-monitoring.git
cd snake-monitoring

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python snake_monitor.py

🎮 Uso
# Modo normal
python snake_monitor.py

# Con configuración personalizada
python snake_monitor.py --config mi_config.json

# Ver ayuda
python snake_monitor.py --help

Atajos de teclado
Tecla                     Acción
q                         Salir
r                         Reiniciar monitoreo
h                         Mostrar ayuda

📸 Capturas
╔═══════════════════════════════════════════╗
║  🐍 SNAKE MONITORING v1.0                ║
╠═══════════════════════════════════════════╣
║  CPU:  ████████░░░░░░  45.2%             ║
║  RAM:  ██████████░░░░  62.7%             ║
║  DISK: ████░░░░░░░░░░  28.1%             ║
║  NET:  ⬆ 1.2MB/s  ⬇ 3.4MB/s            ║
╚═══════════════════════════════════════════╝
