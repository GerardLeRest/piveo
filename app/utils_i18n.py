UI_VALUES = {
    "parlement": "Parlement",
    "parti": "Parti",
    "depute": "Député",
    "commissions": "Commissions",
    "entreprise": "Entreprise",
    "departement": "Département",
    "salarie": "Salarié",
}

def ui_value(value: str) -> str:
    return _(UI_VALUES.get(value, value))
