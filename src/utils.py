import unicodedata

def normalizar(texto):
    """Remove acentos, espaços extras e coloca em maiúsculo para comparação segura."""
    if not texto: 
        return ""
    nfkd_form = unicodedata.normalize('NFKD', str(texto))
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).upper().strip()
