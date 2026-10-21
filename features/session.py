# Identifiant de l'utilisateur actuellement connecté

id_user_actuel = None

def utilisateur_actuel():
    """Indique si un utilisateur est connecté."""
    return id_user_actuel is not None
