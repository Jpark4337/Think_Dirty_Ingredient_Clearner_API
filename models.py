from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Classification = Literal[
    "ingredient",         # A standard INCI chemical or botanical
    "marketing_term",     # Vague or proprietary terms (e.g., "secret moisturizing complex")
    "unknown",            # Ambiguous, rejected, or unidentifiable
    "mixture_or_blend"    # e.g., "Fragrance/Parfum"
]

class IngredientRequest(BaseModel):
    """
    The expected format for the request payload when submitting an ingredient.
    """
    raw: str = Field(..., description="The original, uncleaned ingredient string for normalization.")

class IngredientResponse(BaseModel):
    """
    The strict JSON output model the LLM must adhere to and the final API response format.
    Ensures data consistency and safety across the service.
    """
    raw: str = Field(..., description="The original raw input, echoed for reference.")
    normalized_inci: Optional[str] = Field(None,description="The recognized INCI name. This field MUST be null if the LLM's confidence is low (<0.5) or the ingredient is ambiguous (safety first!).")
    normalized_common: Optional[str] = Field(None, description="A common, user-friendly name, if one exists (e.g., Vitamin C).")
    category: Classification = Field("unknown", description="Classification of the input based on the predefined types.")
    confidence: float = Field(...,description="The LLM's certainty score (0.0 to 1.0) on the normalized result.")
    flags: List[str] = Field([],description="List of issues or observations about the input (e.g., 'typo_suspected', 'contains_concentration').")
    explanation: str = Field(..., description="A concise explanation for the normalization decision or the reason for nulling the INCI name.") #Note for myself that I have to update all of this in the main.py as well.