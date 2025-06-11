from pydantic import BaseModel


class ProductRequest(BaseModel):
    product: str