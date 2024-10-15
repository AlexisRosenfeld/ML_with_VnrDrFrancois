import signal
import time
from ucimlrepo import fetch_ucirepo
from ucimlrepo.fetch import DatasetNotFoundError
import pandas.errors
import urllib.error

# Initialisation des dictionnaires pour stocker les datasets, features, targets et temps d'exécution
dataset = {}
X = {}
y = {}
execution_times = {}  # Dictionnaire pour stocker le temps pris pour chaque dataset

# Liste des identifiants valides
valid_ids = []

# Fonction appelée si le temps imparti est dépassé
def timeout_handler(signum, frame):
    raise TimeoutError

# Assigner la fonction au signal d'alarme
signal.signal(signal.SIGALRM, timeout_handler)

# Boucle pour tester les datasets entre 1 et 100
for i in range(1, 101):
    try:
        # Déclencher une alarme après 4 secondes
        signal.alarm(4)

        # Enregistrer le temps de début
        start_time = time.time()

        # Tester si le dataset est valide
        dataset[i] = fetch_ucirepo(id=i)

        # Si le dataset est valide, ajouter l'identifiant à la liste
        valid_ids.append(i)

        # Stocker les features et les targets dans les dictionnaires
        X[i] = dataset[i].data.features
        y[i] = dataset[i].data.targets

        # Enregistrer le temps de fin et calculer la durée
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times[i] = execution_time

        print(f"Dataset {i} ajouté avec succès en {execution_time:.2f} secondes.")
    
    except TimeoutError:
        # Gérer les cas où la requête prend plus de 4 secondes
        print(f"Dataset {i} a pris trop de temps à charger (plus de 4 secondes).")
    
    except DatasetNotFoundError:
        # Ignorer les datasets non disponibles
        print(f"Dataset {i} n'est pas disponible.")
    
    except pandas.errors.ParserError:
        # Gérer les erreurs de parsing des fichiers CSV
        print(f"Erreur de parsing pour le dataset {i}, problème avec le format du fichier CSV.")
    
    except ConnectionError:
        # Gérer les erreurs de connexion
        print(f"Erreur de connexion au serveur pour le dataset {i}, réessaye plus tard.")
    
    except urllib.error.HTTPError as e:
        # Gérer les erreurs HTTP
        print(f"Erreur HTTP {e.code} pour le dataset {i} : {e.reason}")
    
    finally:
        # Désactiver l'alarme après chaque itération pour éviter qu'elle ne se propage
        signal.alarm(0)

# Afficher la liste des identifiants valides et le temps pris pour chaque dataset
print("Identifiants valides : ", valid_ids)
print("Temps d'exécution par dataset : ", execution_times)


#quand je run j'ai valid_ids = [1, 3, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 27, 28, 29, 30, 32, 33, 39, 40, 42, 43, 44, 45, 46, 47, 50, 52, 53, 58, 59, 60, 62, 63, 70, 74, 78, 81, 82, 83, 87, 88, 89, 90, 91, 92, 95, 96]