import re
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from models import IngredientRequest, IngredientResponse, Classification
from openai_client import get_normalized_ingredient_from_llm # These are the LLM Call functions with retries, but havne't working yet. 

#FastAPI app initilization can be started at here
app = FastAPI(title="Ingredient Normalization Service",
    description="API for standardizing cosmetic ingredient names using a structured LLM approach.",
    version="1.0.0")

# Utility function for cleaning raw input strings
def clean_input(raw_input: str) -> str:
    """Removes leading/trailing spaces, quotes, and collapses internal whitespace."""
    cleaned = raw_input.strip().strip('"').strip("'").strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

@app.post("/v1/ingredient/normalize", response_model=IngredientResponse)
async def normalize_ingredient_endpoint(request: IngredientRequest):
    """
    Normalizes a single raw ingredient string using a structured LLM call.
    Implements crucial safety checks for empty or ambiguous inputs.
    """
    sanitized_input = clean_input(request.raw)

    #Check for Empty Input (The most common error from messy lists)
    if not sanitized_input:
        return IngredientResponse(
            raw=request.raw,
            normalized_inci=None,
            normalized_common=None,
            category="unknown",
            confidence=0.0,
            flags=["empty_input"],
            explanation="Input string was empty after sanitation.")

    # 3. Define the LLM's Role and Prompt
    
    # This system prompt tells the LLM its job, the rules, and the output format.
    system_prompt = (
        "You are an expert cosmetic chemistry standardization engine. "
        "Your task is to normalize a single raw ingredient string into the official INCI name. "
        "Strictly adhere to the provided JSON schema. If an input is ambiguous, contains a high-risk similarity "
        "to a potentially toxic compound (e.g., Chlorite vs. Chloride), or your confidence is below 0.5, "
        "you MUST set 'normalized_inci' to null and set 'confidence' to a low value. "
        "Always prioritize safety and accuracy over forcing a match.")
    
    user_prompt = f"Normalize this raw ingredient string: '{sanitized_input}'"

    json_schema = IngredientResponse.model_json_schema()

    try:
        llm_data_dict = get_normalized_ingredient_from_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_schema=json_schema)
        
        validated_response = IngredientResponse(**llm_data_dict)
        validated_response.raw = request.raw # Ensure the *original* raw input is returned

        return validated_response

    except ValidationError as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM returned invalid data structure. Internal Validation Error: {e}"
        )
    except Exception as e:
        print(f"UNHANDLED API CALL ERROR: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the LLM request: {e}")
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)