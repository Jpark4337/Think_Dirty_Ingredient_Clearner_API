import os
import json
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIError, AuthenticationError
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

load_dotenv()

llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RETRY_ERRORS = (RateLimitError, APIError)

@retry(
    wait=wait_exponential(min=2, max=30),  # Wait starts at 2s, backs off up to 30s
    stop=stop_after_attempt(4),             # Only try a maximum of 4 times total as it would just waste the quota and this was the number that I should put following the project recommendation.
    retry=retry_if_exception_type(RETRY_ERRORS),
    reraise=True # Re-raise the error if all retries fail
)
def call_llm_for_structured_data(
    system_prompt: str,
    user_prompt: str,
    output_schema: dict
) -> dict:
    """
    Handles the API call to OpenAI, requiring structured JSON output.
    Includes automated exponential backoff and retries for common network/rate-limit failures.
    """
    
    print(f"DEBUG: Attempting LLM call for input: '{user_prompt}'")

    try:
        response = llm_client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_model=output_schema,  # <--- NEW AND CORRECT APPROACH for the modern OpenAI client
        )

        return response.model_dump()

    except AuthenticationError as e:
        print("FATAL ERROR: OpenAI API Key is invalid or expired. Cannot authenticate.")
        raise e
        
    except RateLimitError as e:
        print(f"WARNING: Rate limit exceeded. Backing off and retrying...")
        raise e # Handled by tenacity

    except APIError as e:
        print(f"ERROR: General OpenAI API server error. Retrying...")
        raise e # Handled by tenacity

# Renaming the main export function to be more descriptive for main.py
get_normalized_ingredient_from_llm = call_llm_for_structured_data