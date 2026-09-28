from typing import List, Optional
from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6, max_length=128)
    confirm_password: str = Field(min_length=6, max_length=128)

class UserLogin(BaseModel):
    username: str
    password: str

class HomeInput(BaseModel):
    budget: float = Field(gt=0)
    room_type: str = "Living Room"
    lights: int = Field(default=2, ge=0, le=50)
    ceiling_fans: int = Field(default=1, ge=0, le=20)
    furniture: int = Field(default=2, ge=0, le=50)
    dining_tables: int = Field(default=0, ge=0, le=10)
    kitchen_items: int = Field(default=0, ge=0, le=50)
    style: str = "Modern"
    requirements: str = ""

class PartyInput(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0, le=10000)
    event_type: str = "Birthday"
    venue_type: str = "Indoor"
    catering: bool = True
    decoration: bool = True
    entertainment: bool = True
    accommodation: bool = False
    requirements: str = ""

class JewelryInput(BaseModel):
    budget: float = Field(gt=0)
    occasion: str = "Wedding"
    style: str = "Elegant"
    preferences: str = ""

class RecommendationItem(BaseModel):
    name: str
    description: str
    estimated_price: float = Field(ge=0)
    quantity: int = Field(default=1, ge=1)
    platform: str
    search_url: str
    category: str

class BudgetCategory(BaseModel):
    category: str
    allocation: float = Field(ge=0)
    percentage: float = Field(ge=0, le=100)
    items: List[RecommendationItem] = []

class RecommendationResult(BaseModel):
    planner: str
    total_budget: float
    estimated_total: float
    remaining_budget: float
    summary: str
    categories: List[BudgetCategory]
    tips: List[str] = []
    source_note: str = "Prices are AI estimates; verify current prices on the linked platform."
