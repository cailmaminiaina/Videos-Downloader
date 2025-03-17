from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
from urllib.parse import unquote

app = Flask(__name__)

DOWNLOAD_FOLDER = "videos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def telecharger_video(url):
    options = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best'
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = f"{info_dict['title']}.{info_dict['ext']}"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        return filename, filepath

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "Aucune URL fournie"}), 400
    
    try:
        filename, filepath = telecharger_video(url)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/download/<path:url>', methods=['GET'])
def download_get(url):
    """
    Télécharge la vidéo à partir de l'URL passée dans l'URL du serveur.
    """
    # Décode l'URL encodée
    decoded_url = unquote(url)
    
    if not decoded_url.startswith("http"):
        return jsonify({"error": "URL invalide"}), 400

    try:
        # Téléchargement de la vidéo
        filename, filepath = telecharger_video(decoded_url)
        
        # Renvoie le fichier en tant que téléchargement
        return send_file(filepath, as_attachment=True)

    except Exception as e:
        logging.error(f"Erreur dans la fonction 'download_get': {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
