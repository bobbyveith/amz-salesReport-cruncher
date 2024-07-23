from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    parent_asin: Optional[str] = None
    child_asin: Optional[str] = None
    units_sold: Optional[float] = None
    total_sales: Optional[float] = None
    sku: Optional[str] = None
    title: Optional[str] = None
    is_fba: Optional[bool] = None
    is_active: Optional[bool] = None
