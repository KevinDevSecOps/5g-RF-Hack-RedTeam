# 📡 5G RF Hack - Red Team Toolkit

<div align="center">
  <img src="https://img.shields.io/badge/5G_Hacking-Red_Team-FF0000?style=for-the-badge&logo=windowsterminal&logoColor=white">
  <img src="https://img.shields.io/badge/SDR-HackRF_One+-8A2BE2?style=for-the-badge&logo=gnuradio&logoColor=white">
  <img src="https://img.shields.io/badge/License-GPL_3.0-blue?style=for-the-badge&logo=opensourceinitiative&logoColor=white">
  <img src="https://img.shields.io/badge/OSCP-Certified-FF6600?style=for-the-badge&logo=offensive-security&logoColor=white">
</div>

<br>

> **"Si puedes spoofear un gNodeB, el core network es tu patio de juegos."**  
> *— KevinDevSecOps, Red Team Lead*

---

## 🔍 ¿Qué encontrarás aquí?
Herramientas y técnicas para **auditorías de seguridad en redes 5G**, desarrolladas por un equipo de Red Team con certificaciones OSCP/CEH. Todo probado en entornos controlados.

graph TB
    subgraph "Frontend (Python/Flask)"
        A[Dashboard Web]
        B[APIs REST]
        C[Interfaz Usuario]
    end
    
    subgraph "Backend Core (Python)"
        D[Lógica de Negocio]
        E[Gestión de Módulos]
        F[Base de Datos]
    end
    
    subgraph "Componentes Críticos (Rust)"
        G[Procesamiento FPGA]
        H[Auditoría Criptográfica]
        I[Análisis Tiempo Real]
    end
    
    subgraph "Servicios de Red (Go)"
        J[Escaneo Distribuido]
        K[Análisis de Paquetes]
        L[Servicios Network]
    end
    
    A --> B
    B --> D
    D --> G
    D --> J
    G --> I
    J --> K

```python
# Ejemplo de uso ético:
def main():
    target = "5G_SA_Network"
    if authorization_granted(target):
        run_pentest(target)
    else:
        print("⚠️ Obtén permiso por escrito primero.")
```

---

## 🛠️ Toolkit Básico
| Herramienta | Uso | Requisitos |
|-------------|-----|------------|
| **HackRF One+** | Análisis RF (hasta 6GHz) | Antena 3500MHz+ |
| **srsRAN** | Emulación gNodeB | Ubuntu 22.04 |
| **Flipper Zero** | Pruebas físicas (RFID/NFC) | Firmware QF7 |
| **Wireshark** | Captura paquetes 5G | Filtro `ngap` |

---

## 📅 Cronograma de Implementación

| Día | Tarea | Estado |
|-----|-------|--------|
| 1 | Estructura y Dockerización | ✅ |
| 2 | Core Framework | 🚧 |
| 3 | Dashboard Web | 📋 |
| 4 | Integración y Testing | 📋 |
| 5 | Documentación y Release | 📋 |

## 🚀 Para Empezar HOY:

1. **Ejecuta estos comandos:**
```bash
git clone https://github.com/KevinDevSecOps/5g-RF-Hack-RedTeam.git
cd 5g-RF-Hack-RedTeam

# Crear estructura de carpetas
mkdir -p docker src/core src/modules src/dashboard src/utils docs tests templates

# Crear archivos iniciales
touch docker/Dockerfile docker/docker-compose.yml requirements.txt main.py

## 📌 Primeros Pasos
1. **Clona el repo**:
   ```bash
   git clone https://github.com/KevinDevSecOps/5G-RF-Hack-RedTeam.git
   cd 5G-RF-Hack-RedTeam
   ```

2. **Configura entorno** (Kali Linux recomendado):
   ```bash
   sudo apt install gnuradio hackrf python3-srsran
   ```

3. **Ejecuta un test básico**:
   ```bash
   python3 tools/gNodeB_scanner.py --freq 3500M
   ```
# Iniciar con dashboard
python main.py --dashboard

# Escanear espectro
curl -X POST http://localhost:5000/api/scan/start
---

## ⚠️ Aviso Legal
```diff
- IMPORTANTE: Este proyecto es SOLO para:
+ Investigación autorizada
+ Auditorías éticas con consentimiento
+ Educación en seguridad 5G

- Prohibido usar para:
+ Interceptar comunicaciones reales
+ Atacar infraestructura crítica
+ Violar la Ley General de Telecomunicaciones (España/UE)
```

---

## 📂 Estructura del Repo
```mermaid
flowchart LR
    A[/5G-RF-Hack-RedTeam] --> B[/docs]
    A --> C[/attack_scripts]
    A --> D[/detection]
    A --> E[/hardware]
    B --> B1[Threat_Modeling.md]
    C --> C1[gNodeB_spoofer.py]
    D --> D1[sigma_rules]
    E --> E1[HackRF_configs]
```
# 5G RF Hack RedTeam Toolkit

Herramienta completa para pentesting de redes 5G mediante RF.

## 🚀 Características

- Análisis de espectro en tiempo real
- Dashboard web para monitorización
- Dockerizado para fácil deployment
- Módulos de pentesting para 5G

## 📦 Instalación

```bash
# Con Docker
docker-compose -f docker/docker-compose.yml up --build

# Manual
pip install -r requirements.txt
python main.py --dashboard
---

## 🤝 ¿Cómo Contribuir?
1. Abre un **Issue** para discutir nuevas features
2. **Forkea** el proyecto
3. Envía un **PR** con:
   - Scripts documentados
   - Capturas de pruebas (opcional)
   - Referencias a estándares 3GPP

```bash
# Estilo de commits:
git commit -m "feat: [5G] Añade scanner de slicing networks"
```

---

<div align="center">
  <a href="https://github.com/KevinDevSecOps/5G-RF-Hack-RedTeam/issues">
    <img src="https://img.shields.io/badge/¿Preguntas?-Abrir_Issue-FF6600?style=for-the-badge&logo=github">
  </a>
  <a href="https://twitter.com/TuUsuario">
    <img src="https://img.shields.io/badge/Contacto-DM_@TuUsuario-1DA1F2?style=for-the-badge&logo=twitter">
  </a>
</div>

<br>

> **Disclaimer:** El autor no se hace responsable del mal uso de estas herramientas.  
> *«Con gran poder RF viene gran responsabilidad»* 🕷️
```

---
> **Nota sobre BadUSB**: Estos payloads pueden violar leyes de telecomunicaciones.  
> - Úsalos SOLO en dispositivos de tu propiedad.  
> - Consulta la [Ley General de Telecomunicaciones (España)](https://www.boe.es/eli/es/l/2014/05/09/9).

> ⚠️ **ADVERTENCIA**:  
> - El bypass biométrico solo debe probarse en dispositivos de tu propiedad.  
> - La manipulación de sistemas de reconocimiento facial puede violar el **RGPD (UE 2016/679)**.  
> - Estos scripts son para auditorías autorizadas. Consulta siempre con el departamento legal.
