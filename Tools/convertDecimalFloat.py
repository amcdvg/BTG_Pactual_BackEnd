from typing import List, Dict, Any
from decimal import Decimal

def convertDecimalFloat(data: Any) -> Any:
    """Convierte Decimals a floats recursivamente."""
    if isinstance(data, dict):
        return {k:  convertDecimalFloat(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [ convertDecimalFloat(i) for i in data]
    elif isinstance(data, Decimal):
        return float(data)
    return data