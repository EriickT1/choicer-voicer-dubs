import sys
import os
import subprocess
import shutil
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_dubs.py <WORK_DIR>")
        sys.exit(1)
        
    workdir = os.path.abspath(sys.argv[1])
    mapping_file = os.path.join(workdir, "mapping.json")
    video_path = os.path.join(workdir, "videoplayback.mp4")
    no_vocals_wav = os.path.join(workdir, "separated", "htdemucs", "videoplayback", "no_vocals.wav")
    vocals_wav = os.path.join(workdir, "separated", "htdemucs", "videoplayback", "vocals.wav")
    
    if not os.path.exists(mapping_file):
        print(f"Error: {mapping_file} not found.")
        sys.exit(1)
        
    with open(mapping_file, "r", encoding="utf-8") as f:
        segments = json.load(f)
        
    OUTPUT_DIR = os.path.join(workdir, "ChoicerVoicer_Output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("[*] Extracting dub_video.ogv...")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, 
        "-c:v", "libtheora", "-q:v", "7", "-an", 
        os.path.join(OUTPUT_DIR, "dub_video.ogv")
    ], check=True)

    print("[*] Generating _backing_track.mp3...")
    subprocess.run([
        "ffmpeg", "-y", "-i", no_vocals_wav,
        "-q:a", "2", 
        os.path.join(OUTPUT_DIR, "_backing_track.mp3")
    ], check=True)

    print("[*] Creating _pack_info.ini...")
    pack_info = f"""[data]\n\ntitle="Dubbing Pack"\nicon="icon.jpg"\nauthors=["Skill Choicer Voicer"]\n"""
    with open(os.path.join(OUTPUT_DIR, "_pack_info.ini"), "w", encoding="utf-8") as f:
        f.write(pack_info)

    for seg in segments:
        char_key = seg.get('char_key', 'unknown').lower().replace(' ', '_')
        char_name = seg.get('char_name', 'Unknown')
        if not char_key:
            char_key = "unknown"
        
        prefix = f"{seg['id']:02d}_{char_key}"
        print(f"Processing {prefix}...")
        
        duration = seg['end'] - seg['start']
        
        # Audio extraction
        subprocess.run([
            "ffmpeg", "-y", "-i", vocals_wav,
            "-ss", str(seg['start']), "-t", str(duration),
            "-q:a", "2",
            os.path.join(OUTPUT_DIR, f"{prefix}.mp3")
        ], check=True)
        
        # Image extraction
        frame_time = seg['start'] + min(1.0, duration / 2) 
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path,
            "-ss", str(frame_time), "-vframes", "1",
            "-q:v", "2",
            os.path.join(OUTPUT_DIR, f"{prefix}.jpg")
        ], check=True)
        
        # INI Creation
        ini_content = f"""[data]\n\ncaption="“{seg['text']}”"\ndub_timestamps=[{seg['start']:.3f}]\ndub_characters=["{char_name}"]\n"""
        with open(os.path.join(OUTPUT_DIR, f"{prefix}.ini"), "w", encoding="utf-8") as f:
            f.write(ini_content)
            
        if seg['id'] == 1:
            shutil.copy(
                os.path.join(OUTPUT_DIR, f"{prefix}.jpg"),
                os.path.join(OUTPUT_DIR, "icon.jpg")
            )

    print(f"\n[+] Paquete generado con éxito en: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
