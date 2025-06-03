from flask import render_template, request, redirect, url_for,flash
from app import app, db
from app.models import Categorie

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
