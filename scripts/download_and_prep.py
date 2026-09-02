import sys
import os
import subprocess
import json
import urllib.parse
import re

def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    return "unknown_video"

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_and_prep.py <YOUTUBE_URL>")
        sys.exit(1)
        
    url = sys.argv[1]
    vid_id = get_video_id(url)
    workdir = os.path.abspath(os.path.join("workdir", vid_id))
    os.makedirs(workdir, exist_ok=True)
    
    video_path = os.path.join(workdir, "videoplayback.mp4")
    
    print(f"[*] Downloading {url} to {video_path}...")
    subprocess.run([
        sys.executable, "-m", "yt_dlp", 
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "-o", video_path,
        url
    ], check=True)
    
    print("[*] Running Demucs to separate vocals...")
    subprocess.run([
        sys.executable, "-m", "demucs",
        "--two-stems=vocals",
        "-o", os.path.join(workdir, "separated"),
        video_path
    ], check=True)
    
    vocals_wav = os.path.join(workdir, "separated", "htdemucs", "videoplayback", "vocals.wav")
    
    print("[*] Running Whisper for transcription...")
    subprocess.run([
        sys.executable, "-m", "whisper",
        vocals_wav,
        "--language", "es",
        "--output_format", "json",
        "--model", "base",
        "--output_dir", workdir
    ], check=True)
    
    whisper_json = os.path.join(workdir, "vocals.json")
    print(f"[*] Reading Whisper output from {whisper_json}...")
    
    with open(whisper_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    mapping = []
    for i, seg in enumerate(data.get("segments", [])):
        mapping.append({
            "id": i + 1,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
            "char_key": "",
            "char_name": ""
        })
        
    mapping_file = os.path.join(workdir, "mapping.json")
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4, ensure_ascii=False)
        
    print(f"\n[+] Preparación completada!")
    print(f"[+] Revisa y edita {mapping_file} para asignar los personajes.")

if __name__ == "__main__":
    main()
