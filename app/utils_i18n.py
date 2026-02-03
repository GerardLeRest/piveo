from gettext import gettext as _

UI_VALUES = {
    "parlement": _("Parlement"),
    "parti": _("Parti"),
    "depute": _("Député"),
    "commissions": _("Commissions"),
    "entreprise": _("Entreprise"),
    "departement": _("Département"),
    "salarie": _("Salarié"),
}

def ui_value(value: str) -> str:
    """
    Retourne la valeur affichable traduite pour l'UI.
    Si la valeur n'est pas connue, on retourne la valeur brute.
    """
    return UI_VALUES.get(value, value)

