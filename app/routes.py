from flask import render_template, request, redirect, url_for,flash
from app import app, db
from app.models import Categorie
import pandas as pd
from werkzeug.utils import secure_filename
import os

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nom = request.form["nom"].strip()
        quantite = int(request.form["quantite"])

        cat = Categorie.query.filter_by(nom=nom).first()
        if cat:
            cat.quantite += quantite
        else:
            cat = Categorie(nom=nom, quantite=quantite)
            db.session.add(cat)

        db.session.commit()
        return redirect(url_for("index"))

    categories = Categorie.query.all()
    return render_template("index.html", categories=categories)

@app.route('/increment/<int:cat_id>', methods=['POST'])
def increment_quantity(cat_id):
    cat = Categorie.query.get_or_404(cat_id)
    cat.quantite += 1
    db.session.commit()
    flash(f"Quantité de '{cat.nom}' augmentée.", "success")
    return redirect(url_for('index'))  # ou la route principale de ton app

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Créer le dossier s’il n’existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/import', methods=['POST'])
def import_excel():
    if 'excel_file' not in request.files:
        flash("Aucun fichier sélectionné", "error")
        return redirect(url_for('index'))

    file = request.files['excel_file']
    if file.filename == '':
        flash("Fichier invalide", "error")
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Lire le fichier Excel
    try:
        df = pd.read_excel(filepath)
        for _, row in df.iterrows():
            nom = str(row['nom']).strip()
            quantite = int(row['quantite'])

            # Cherche si la catégorie existe déjà
            existing = Categorie.query.filter_by(nom=nom).first()
            if existing:
                existing.quantite += quantite
            else:
                new_cat = Categorie(nom=nom, quantite=quantite)
                db.session.add(new_cat)

        db.session.commit()
        flash("Données importées avec succès", "success")
    except Exception as e:
        flash(f"Erreur lors de l’importation : {e}", "error")

    return redirect(url_for('index'))
