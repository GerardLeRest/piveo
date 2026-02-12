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
