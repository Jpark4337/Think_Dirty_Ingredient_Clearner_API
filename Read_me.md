# Goal

Build a tiny HTTP API your backend can call to turn messy, user- or supplier-provided ingredient strings into a normalized ingredient object.

## Plan

| Phase | Status |
| :--- | :--- |
| Setup & Models | **Completed** |
| LLM Client & Retry | **Completed** |
| FastAPI Integration & Prompting (main.py) | **Completed** |
| Documentation (README.md) | **Completed** |
| Testing (Unit Tests) | **Pending** |

## AI USE

Tool: Google Gemini and Chat GPT

## Prompt v1: Project Initialization

"I am working on this and can you tell me step by step to work on the project? From the project description, I think this is very similar case from my first project but I have to code for this time. The input dataset is the same as the first project, but I have given the API contract which is : API contract
Endpoint
POST /v1/ingredient/normalize
Request JSON
Response JSON (strict shape)
Rules
normalized_inci: return the best-guess INCI name only if you’re confident. Otherwise null.
confidence: 0–1 numeric.
flags: examples: ["typo_suspected", "ambiguous", "derivative_vs_parent", "not_inci", "contains_concentration", "potentially_wrong_merge"]
explanation: 1–3 sentences for humans (this is for internal review / debugging)."
Change Log / Iteration: 1
Result: AI provided the full directory structure and terminal commands to set up the environment. Gave me the plan for the project: Setup & Models, LLM Client & Retry, FastAPI Integration & Prompting (main.py),Testing (Unit Tests), Documentation Final.

Change log: I accepted the file structure but had to manually create the files. such as venv, .env file, gitignore.

## Prompt v2

I have install the venv, .env file, gitignore, but what are these as conceptually? I do not understand what I am doing right now so can you please explain what these are for?

Iteration: 1

Change log: I had to understand what is going on so that I can explain what I have done and read the code and what each codes are. For example, I realized gitignore file is preventing the venv file to be uploaded to Github as they are too big file to be pushed into Github

## Prompt v3

"Can you please give me the code for main.py, mdoels.py, openai_client.py files so that I can see how they works and I will change the code later if there is a specific change that I want to change but I want to check if I will be able to start the server and move to Unit Testing. If this works it means there is possibility that I can finish this project in a day."

Iteration: 1

Change log: 
-Result: Received the complete initial code for `main.py`, `models.py`, and `openai_client.py`.

-The server immediately failed to start, throwing an `ImportError` or `ModuleNotFoundError` (as detailed in Prompt v4) because the files were either named incorrectly or not visible to the Python interpreter.

## Prompt v4  

"I got this error : (venv) jaypark@Jays-MacBook-Pro ... Traceback (most recent call last): ... ModuleNotFoundError: No module named 'models'" Can you please explain what is wrong and what I should do?
Issue: The code failed to run because of a casing mismatch (Main.py vs main.py) and a missing file issue."

Fix: The AI identified that my file was named Main.py (capitalized) and that models.py was empty/missing so I had to make the new one.

Change log: I renamed the file to main.py and populated models.py with the Pydantic schemas.

## Prompt v5

Prompt v1: "Now I can work on server but I am having this error message on terminal can you please why I am getting this error and please let me know how I should solve this problem? Here is the error message : Calling LLM for raw input: 'Phenoxyehtanol' ... UNHANDLED API CALL ERROR: Error code: 404 - {'error': {'message': 'The model gpt-4-turbo does not exist or you do not have access to it.' ...}}"

Prompt v2: "Does this mean that there is an error but also there is a problem with the billing issue with OpenAI? What if I change the virsion of the OpenAI gpt version? I am pretty sure there is the free-version for the users but do you think it would work to solve this problem?"

Change Log / Iteration: 2 (I tried to figure out how to solve the billing issue, but I have used all of my quota so I could not figure out the alternative way other than paying for this project)

v1: The initial code used a model name (gpt-4-turbo) that my specific API key did not have access to. So I have iterated through model names in my openai_client .py file to "gpt-3.5-turbo-0125" version to see if this works as free version.

v2: The answer was no. The model implemented in the client, gpt-3.5-turbo-0125, was deliberately chosen because it is one of the most stable, cost-efficient, and capable GPT-3.5 models available, offering reliable support for the structured JSON output required by the API. While this model typically includes the most generous free trial usage, the final error encountered—Error code: 429 insufficient_quota—confirms that all available credits for the external OpenAI API have been exhausted.

## Prompt v6

"I am getting this error for Live API Test Confirmation: can you please explain why this is not working. Here is the error: (venv) jaypark@Jays-MacBook-Pro Think_Dirty_Ingredient_Clearner_API % python main.py
Traceback (most recent call last):
  File "/Users/jaypark/Desktop/Computer Science Project/Think_Dirty_Ingredient_Clearner_API/main.py", line 7, in module
    from models import IngredientRequest, IngredientResponse, CategoryType
ImportError: cannot import name 'CategoryType' from 'models' (/Users/jaypark/Desktop/Computer Science Project/Think_Dirty_Ingredient_Clearner_API/models.py)"

Issue: My main.py script is trying to import CategoryType, but the file it is importing from models.py only defines a type called Classification.

Iteration: 1

Change log 1. I have changed the script and it works now.
