from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

# Crée le dossier de téléchargement s'il n'existe pas déjà
DOWNLOAD_FOLDER = "videos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Page d'accueil avec le formulaire
@app.route('/')
def index():
    """
    Affiche la page d'accueil avec un formulaire pour entrer l'URL de la vidéo.
    """
    return render_template('index.html')

def telecharger_video(url):
    """
    Télécharge la vidéo à partir de l'URL fournie et retourne le nom et chemin du fichier.
    """
    options = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = f"{info_dict['title']}.{info_dict['ext']}"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        return filename, filepath

# Route pour télécharger la vidéo via un formulaire POST
@app.route('/download', methods=['POST'])
def download():
    # Tentative d'obtenir l'URL soit par formulaire, soit par JSON
    url = request.form.get("url")  # Méthode 1: via le formulaire HTML
    if not url:
        data = request.json  # Méthode 2: via JSON
        url = data.get("url") if data else None

    if not url:
        return jsonify({"error": "Aucune URL fournie"}), 400
    
    try:
        filename, filepath = telecharger_video(url)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
