from pydantic import BaseModel, Field
from typing import Optional, List


class Movie(BaseModel):

    id: Optional[int] = None
    tittle: str = Field(max_length=15)
    overview: str = Field(max_length=15)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(max_length=15)