from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    name: str
    price: str
    description: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
