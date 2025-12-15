# Goal

Build a tiny HTTP API your backend can call to turn messy, user- or supplier-provided ingredient strings into a normalized ingredient object.

# Plan

Phase                  Status
Setup & Models         Completed
LLM Client & Retry     Completed
FastAPI Integration & Prompting (main.py)               Current Focus
Testing (Unit Tests)    Next
Documentation (Readme.md) Final
# AI USE
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
Action: I accepted the file structure but had to manually create the files. such as venv, .env file, gitignore.

## Prompt v2: 
I have install the venv, .env file, gitignore, but what are these as conceptually? I do not understand what I am doing right now so can you please explain what these are for? 
Iteration: 1
Outcome: I had to understand what is going on so that I can explain what I have done and read the code and what each codes are. For example, I realized gitignore file is preventing the venv file to be uploaded to Github as they are too big file to be pushed into Github

## Prompt v3: 
Can you please give me the code for main.py, mdoels.py, openai_client.py files so that I can see how they works and I will change the code later if there is a specific change that I want to change but I want to check if I will be able to start the server and move to Unit Testing. If this works it means there is possibility that I can finish this project in a day.
Iteration: 1
Outcome: I have got the error that I do not have module "model"

## Prompt v4:  
"I got this error : (venv) jaypark@Jays-MacBook-Pro ... Traceback (most recent call last): ... ModuleNotFoundError: No module named 'models'" Can you please explain what is wrong and what I should do?
Issue: The code failed to run because of a casing mismatch (Main.py vs main.py) and a missing file issue.
Fix: The AI identified that my file was named Main.py (capitalized) and that models.py was empty/missing so I had to make the new one.
Outcome: I renamed the file to main.py and populated models.py with the Pydantic schemas.

## Prompt v5: 
" Now I can work on server but I am having this error message on terminal can you please why I am getting this error and please let me know how I should solve this problem? Here is the error message : Calling LLM for raw input: 'Phenoxyehtanol' ... UNHANDLED API CALL ERROR: Error code: 404 - {'error': {'message': 'The model gpt-4-turbo does not exist or you do not have access to it.' ...}}"

Change Log / Iteration: 2 (I tried to figure out how to solve this problem but I am stuck)
Issue: The initial code used a model name (gpt-4-turbo) that my specific API key did not have access to.
I have tried iterated through model names in my oepnai_client.py file. I rejected the prompt suggesting gpt-4-turbo and accepted the fix to switch to gpt-3.5-turbo-0125, but this have not solved the problem yet.