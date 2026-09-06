import pandas as pd

MANUFACTURER_MAPPING = {
    'MERCEDES-BENZ': 'DAIMLER',
    'DAIMLER BUSES': 'DAIMLER',
    'MERCEDES': 'DAIMLER',
    'M A N': 'MAN'
}

RULES = {}

def register(name):
    def decorator(func):
        RULES[name] = func
        return func
    return decorator

@register('invalid_count')
def rule_invalid_bus_count(df: pd.DataFrame) -> pd.Series:
    """
    Rule to find invalid rows. Returns a boolean Series where True means the row is invalid.
    """
    return df['Anzahl'] <= 0

@register('missing_mfg')
def rule_missing_manufacturer(df: pd.DataFrame) -> pd.Series:
    """Rule to find rows with a missing manufacturer after cleaning."""
    return df['Hersteller_Clean'].isna()