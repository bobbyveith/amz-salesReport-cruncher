from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    parent_asin: Optional[str] = None
    child_asin: Optional[str] = None
    units_sold: Optional[float] = None
    total_sales: Optional[float] = None
    sku: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    title: Optional[str] = None
    aspect_ratio: Optional[str] = None
    is_fba: Optional[bool] = None
    is_active: Optional[bool] = None

if __name__ == "__main__":
    print("[X] Warning: This module is not meant to be run directly!")