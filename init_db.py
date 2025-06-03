from app import app, db
from app.models import Categorie  # Assure-toi d'importer les modèles

# Active le contexte d'application pour utiliser db
with app.app_context():
    db.create_all()
    print("✔ Base de données initialisée avec succès.")
