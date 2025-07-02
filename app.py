# app.py
from flask import Flask, request, send_file, jsonify, render_template
from yt_dlp import YoutubeDL
from werkzeug.utils import secure_filename
import os
import traceback

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_file('index.html')

@app.route("/formats", methods=["POST"])
def get_formats():
    try:
        url = request.json.get("url")
        if not url:
            return jsonify({"error": "URL no proporcionada"}), 400

        ydl_opts = {
            'ffmpeg_location': r'C:\Users\santi\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin',
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            available_formats = info["formats"]

            formats = []

            for f in available_formats:
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    formats.append({
                        "format_id": f["format_id"],
                        "ext": f["ext"],
                        "resolution": f.get("resolution") or f"{f.get('height', '?')}p",
                        "fps": f.get("fps"),
                        "filesize": f.get("filesize"),
                        "vcodec": f.get("vcodec"),
                        "acodec": f.get("acodec"),
                    })
            
            # Añadir formatos combinados para alta resolución
            video_formats = [f for f in available_formats if f.get("vcodec") != "none" and f.get("height") and f.get("height") >= 720]
            best_audio = next((f for f in available_formats if f.get("acodec") != "none" and f.get("vcodec") == "none"), None)
            
            if best_audio:
                for vf in video_formats:
                    # Solo añadir si no existe ya un formato con esta resolución y audio
                    if not any(f["resolution"] == (vf.get("resolution") or f"{vf.get('height', '?')}p") and f["acodec"] != "none" for f in formats):
                        formats.append({
                            "format_id": f"{vf['format_id']}+{best_audio['format_id']}",
                            "ext": "mp4",
                            "resolution": vf.get("resolution") or f"{vf.get('height', '?')}p",
                            "fps": vf.get("fps"),
                            "filesize": (vf.get("filesize") or 0) + (best_audio.get("filesize") or 0),
                            "vcodec": vf.get("vcodec"),
                            "acodec": best_audio.get("acodec"),
                            "combined": True
                        })
            
            # Ordenar por resolución (altura) de mayor a menor
            formats.sort(key=lambda x: int(x["resolution"].replace("p", "")) if x["resolution"].replace("p", "").isdigit() else 0, reverse=True)
            
            return jsonify({"formats": formats})
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": f"Error al obtener formatos: {str(e)}"}), 500

@app.route("/download", methods=["POST"])
def download_video():
    try:
        url = request.json.get("url")
        format_id = request.json.get("format_id")
        
        if not url:
            return jsonify({"error": "URL no proporcionada"}), 400
        if not format_id:
            return jsonify({"error": "Formato no proporcionado"}), 400

        output_path = "downloads"
        os.makedirs(output_path, exist_ok=True)

        # Configuración para descargar con la mejor calidad de audio
        ydl_opts = {
            'format': format_id,
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'ffmpeg_location': r'C:\Users\santi\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if info.get("ext") != "mp4":
                filename = os.path.splitext(filename)[0] + ".mp4"
                
            if not os.path.exists(filename):
                # Intenta encontrar el archivo con la extensión correcta
                base_filename = os.path.splitext(filename)[0]
                for ext in [".mp4", ".webm", ".mkv"]:
                    if os.path.exists(base_filename + ext):
                        filename = base_filename + ext
                        break
            
            if not os.path.exists(filename):
                return jsonify({"error": f"No se pudo encontrar el archivo descargado: {filename}"}), 500
            
            title = info.get('title', 'video')
            safe = secure_filename(title) + '.mp4'

            # Renombra el fichero en disco (opcional, mejora legibilidad):
            os.replace(filename, os.path.join(output_path, safe))
            filename = os.path.join(output_path, safe)
                
            return send_file(
                filename,
                as_attachment=True,
                download_name=safe,
                mimetype='video/mp4'
            )
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": f"Error al descargar: {str(e)}"}), 500

if __name__ == "__main__":
    # Asegurarse de que exista la carpeta de descargas
    os.makedirs(os.path.join(os.getcwd(), "downloads"), exist_ok=True)
    app.run(debug=True)
