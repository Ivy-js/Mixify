from flask import Blueprint, redirect, request, session, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from .downloader import get_mp3


main = Blueprint("main", __name__) 


sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"), 
    scope="playlist-read-private playlist-read-collaborative"
)

@main.route("/")
def index():
    return "<a href='/login'>Se connecter avec Spotify</a>"

@main.route("/login")
def login(): 
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)
@main.route("/callback")
def callback(): 
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("main.playlists"))

@main.route("/playlists")
def playlists(): 
    token_info = session.get("token_info", None)
    if not token_info: 
        return redirect(url_for("main.login"))
    
    sp = spotipy.Spotify(auth=token_info["access_token"])
    playlists = sp.current_user_playlists()
    html = "<h2>Vos Playlists Spotify</h2><ul>"
    for playlist in playlists["items"]:
        html += f"<li>{playlist['name']}</li>"
    html += "</ul>"
    return html


@main.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "Aucune URL fournie", 400
        try:
            filepath = get_mp3(url)
            filename = os.path.basename(filepath)
            return f"<p>Téléchargement réussi : {filename}</p><a href='/download'>Retour</a>"
        except Exception as e:
            return f"<p>Erreur pendant le téléchargement : {e}</p><a href='/download'>Retour</a>"

    # Formulaire HTML
    return '''
        <h2>Télécharger un son depuis une URL</h2>
        <form method="POST" action="/download">
            <label>URL YouTube ou SoundCloud :</label><br>
            <input name="url" size="60" required/><br><br>
            <button type="submit">Télécharger</button>
        </form>
        <br>
        <a href="/">Retour à l'accueil</a>
    '''