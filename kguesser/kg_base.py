import os

class KG_base():
    """Classe "abstraite" pour k-guesser.
    Contient des méthodes communes.
    
    - 'log()'     permet de journaliser les opérations,
                  en console ou dans un fichier.
    - 'params()'  permet d'obtenir et de modifier les 
                  propriétés (publiques) de l'instance.
    """
    def __init__(self):
        self.log_path = ""

    def log(self, txt, f="", end="\n"):
        """Journalise les opérations.
        Permet d'écrire dans un fichier ou au moins évite les 'print'
        dans le code, généralement utilisés pour débugger."""
        f = self.log_path if not f else f
        if f:
            mode = "w" if not os.path.isfile(f) else "a"
            with open(f, mode=mode, encoding="utf-8") as wf:
                wf.write(txt+end)
        else:
            print(txt, end=end)

    def params(self, d_params={}):
        """Fournit les paramètres de la classe.
        Permet aussi de changer ces paramètres."""
        d_cpy = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):     # pas de propriété privée
                continue
            d_cpy[k] = v
        for k, v in d_params.items(): # édition de propriété
            if k in d_cpy:
                d_cpy[k] = self.__dict__[k] = v
        return d_cpy                  # copie par sécurité


