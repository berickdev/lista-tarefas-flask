from flask import Blueprint, render_template, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def pagina_inicial():
    nome = "Bruno Erick"
    return render_template('index.html', nome=nome)