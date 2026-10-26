# Identifiant de l'utilisateur actuellement connecté
user_actuel = None

def utilisateur_actuel():
    """Indique si un utilisateur est connecté."""
    return user_actuel is not None
