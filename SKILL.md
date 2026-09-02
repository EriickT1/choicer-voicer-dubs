---
name: choicer-voicer-dubs
description: >-
  Use this skill to automate the creation of Choicer Voicer dubbing packages from a YouTube URL.
  The skill downloads the video, separates audio, transcribes it, allows the user to assign characters,
  and packages everything (.ini, .mp3, .jpg, .ogv) for the dubbing engine.
---

# Skill: Choicer Voicer Dubs Generator

Este skill automatiza la generación de un paquete completo de recursos para "Choicer Voicer" a partir de un video de YouTube.

## Requisitos Previos (Instalados automáticamente en el paso 1)
- `yt-dlp` (para descargas)
- `demucs` (para separar las voces del fondo)
- `openai-whisper` (para transcripción y timestamps)
- `ffmpeg-python` (y `ffmpeg` instalado en el sistema)

## Flujo de Trabajo (Instrucciones para el Agente)

Para ejecutar este proceso, sigue estos pasos secuenciales:

### Paso 1: Preparación (Descarga, Separación y Transcripción)
Ejecuta el script de preparación pasándole la URL de YouTube que el usuario proporcionó.
Este paso descargará el video, extraerá el audio, separará las voces usando Demucs, lo transcribirá usando Whisper y generará un archivo `mapping.json` preliminar en la carpeta temporal.

```bash
python scripts/download_and_prep.py "URL_DEL_VIDEO"
```
*(Nota: El script creará un directorio de trabajo basado en el ID del video y dejará allí el `mapping.json`).*

### Paso 2: Revisión de Personajes
1. Lee el archivo `mapping.json` recién generado. 
2. Muéstrale al usuario las líneas transcritas y pídele que asigne un **Nombre de Personaje** y un **Identificador Corto** (`char_key`) para cada segmento, O utiliza tu capacidad de deducción de LLM si el usuario ya te proveyó el guion/contexto.
3. Actualiza el archivo `mapping.json` escribiendo los personajes correctos en cada campo `"char_name"` y `"char_key"`.

### Paso 3: Generación del Paquete
Ejecuta el script de generación apuntando a la carpeta de trabajo donde se encuentra el `mapping.json` actualizado.
Esto recortará todos los audios y videos, e inicializará los `.ini`.

```bash
python scripts/generate_dubs.py "ruta/a/la/carpeta/del/video"
```

El script finalizará mostrando la ubicación de la carpeta `ChoicerVoicer_Output` lista para usarse.
