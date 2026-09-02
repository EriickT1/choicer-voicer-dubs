# Choicer Voicer Dubs Skill

¡Bienvenido al Skill de **Choicer Voicer Dubs** para [Antigravity](https://github.com/tu_usuario/antigravity)! 
Este skill le enseña a tu agente de Inteligencia Artificial cómo automatizar la creación de paquetes de recursos (audio, video silenciado, miniaturas y metadatos) necesarios para hacer doblajes en Choicer Voicer a partir de cualquier video de YouTube.

## 🚀 Quickstart (Guía Rápida)

Sigue estos pasos para instalar y empezar a utilizar este Skill con tu agente AI:

### 1. Instalación del Skill
Debes clonar este repositorio dentro de la carpeta de configuraciones de agentes (`.agents/skills/`) de tu proyecto actual:

```bash
# Navega a la raíz de tu proyecto
mkdir -p .agents/skills
cd .agents/skills

# Clona el repositorio del skill
git clone https://github.com/TU_USUARIO/choicer-voicer-dubs.git
```

### 2. Instalación de Dependencias
El skill requiere algunas librerías externas (como `yt-dlp`, `whisper` y `demucs`) para poder descargar, separar el audio y transcribirlo. Pídele a tu agente que las instale, o instálalas tú mismo ejecutando:

```bash
cd choicer-voicer-dubs
pip install -r requirements.txt
```
*(Asegúrate también de tener `ffmpeg` instalado en tu sistema).*

### 3. ¡Úsalo con tu Agente!
Una vez instalado, el agente de Antigravity detectará automáticamente este Skill. Para utilizarlo, simplemente háblale a tu agente en el chat y dale una instrucción como esta:

> **"Quiero usar el skill de choicer-voicer-dubs para crear los dubs de este video: https://www.youtube.com/watch?v=crg8ElS0Xz8"**

### ¿Qué hará el agente?
1. **Descarga y Transcripción:** El agente descargará el video, separará las voces del fondo y transcribirá el audio automáticamente.
2. **Revisión (Interactivo):** El agente hará una pausa y te mostrará el guion que generó. Te pedirá que valides que la transcripción sea correcta y que le indiques qué personaje dice cada frase.
3. **Generación Final:** Una vez que le confirmes los personajes, el agente recortará mágicamente todos los audios, extraerá las imágenes y armará la estructura de carpetas lista para tu doblaje.

---
*Este skill fue generado y optimizado para automatizar por completo el flujo de trabajo de Choicer Voicer.*
