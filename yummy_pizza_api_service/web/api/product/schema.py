from typing import List, Optional
from pydantic import BaseModel


class ProductOptionModelDTO(BaseModel):
    id: Optional[int]
    name: str
    description: str
    extra_charge: float
    option_kind: str
    max_count: Optional[int]
    min_count: Optional[int]
    kal: Optional[float]
    option_sets: Optional[List[str]]

    class Config:
        orm_mode = True


class ProductModelDTO(BaseModel):
    """
    DTO for Product models.

    It returned when accessing Product models from the API.
    """

    id: int
    name: str
    description: str
    item_type: str
    category: str
    kal: float
    price_value: float
    rate: float
    options: Optional[List[ProductOptionModelDTO]]

    class Config:
        orm_mode = True


class ProductModelInputDTO(BaseModel):
    """DTO for creating new product model."""
    id: Optional[int]
    name: str
    description: str
    item_type: str
    category: str
    kal: float
    price_value: float
    rate: float
    options: Optional[List[ProductOptionModelDTO]]

    class Config:
        orm_mode = True