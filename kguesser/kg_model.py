import os, joblib
import pandas as pd
from kg_base import KG_base
from sklearn.model_selection import train_test_split as sk_tts
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as sk_mse
from skleanr.metrics import r2_score as sk_r2
from sklearn.model_selection import cross_val_score as sk_cross

class KG_model(KG_base):
    """Génère, entraîne et teste le modèle.
    Pour le moment, ne gère que la régression linéaire.
    
    - 'fit/predict()' reprennent la librairie scikit-learn.
    - 'test()' teste la précision du modèle.
    - 'preprocess()' gère les variables catégorielles et le 'scaling'.
    - 'select()' fait de la 'feature selection'.
    
    Dans le futur, la classe devrait aussi gérer d'autres modèles 
    quantitatifs pour le projet k-guesser, et permettre de continuer
    l'entraînement d'un modèle existant via 'river' (?)."""
    
    def __init__(self):
        super().__init__()
        self.m = None
        self.m_path = "regression_model.pkl"
    
        # Sauvegarde/chargement #
        #-----------------------#
    def save_m(self, f):
        """Sauvegarde le modèle via joblib."""
        joblib.dump(self.m, f)
    def load_m(self, f):
        """Récupère le modèle sauvegardé via joblib.
        Attention, c'est une faille de sécurité."""
        f = self.m_path if not f else f
        self.m = joblib.load(f) if os.path.isfile(f) else self.m

        # Pré-traitement #
        #----------------#
    def select(self, x, y):
        """Sélectionne les variables 'x' à conserver."""
        nx = x
        return nx
    def preprocess(self, x):
        """Variables catégorielles et équilibrage.
        Note : on assume que le jeu de données est propre."""
        # categoricals
        # scaling
        return x
    
        # Fit/predict #
        #-------------#
    def fit(self, x, y):
        """Entraîne le modèle.
        Note : on ne peut pas encore 'continuer' l'entraînement du modèle."""
        self.m = LinearRegression()           # initialisation
        self.m.fit(x, x)                      # entraînement
    def predict(self, x):
        """Retourne le 'best_k'."""
        return self.m.predict(x)              # prédiction
    def eval(self, x, y):
        """Évalue le modèle déjà entraîné, sans validation croisée."""
        yp = self.predict(x)                  # évaluation
        return sk_mse(y, yp), sk_r2(y, yp)    # MSE et R2

        # Méthode principale #
        #--------------------#
    def test(self, x, y, verbose=True):
        """Méthode générale pour tester le modèle 
        à partir d'un jeu de données."""
        x = self.preprocess(x)                # pré-traitement
        x = self.select(x, y)                 # sélection de variables
        x_tr, x_val, y_tr, y_val = sk_tts(x, y) # entraînement/validation
        self.m = LinearRegression()
        sc = sk_cross(self.m, x_tr, y_tr, cv=5) # validation croisée
        self.fit(x_tr, y_tr)                  # on utilise toutes les données
        mse, r2 = self.eval(x_te, y_te)       # évaluation générale
        if verbose:
            self.log(
                "Model Performance:\n"+
                f"Cross-validation mean: {sc.mean():.02f} "
                f", std: {sc.std():.02f}\n"+
                f"Mean Squared Error: {mse:.02f}\n"+
                f"R² Score: {r2:.02f}\n"
            )
        return sc, mse, r2

