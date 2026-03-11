# ⚠️ IMPORTANT
# ligne ci-dessous -> fonctionnement NORMAL
from builtins import _
# Deux lignes ci-dessous décommmentée -> test if __name__ == "__name__":
# import gettext
# _ = gettext.gettext

LIBELLES_INTERFACE = {
    "parlement": "Parlement",
    "parti": "Parti",
    "depute": "Député",
    "commissions": "Commissions",
    "entreprise": "Entreprise",
    "departement": "Département",
    "salarie": "Salarié",
}

def libelle(value: str) -> str:
    return _(LIBELLES_INTERFACE.get(value, value))
