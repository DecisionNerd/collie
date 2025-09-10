# Collie Project Todo List

## Current Tasks

### Project Structure
- [x] Move code into src folder structure

### Ready to Run
- [x] Application is ready to run with .env file configured

### Bug Fixes
- [x] Handle missing GOOGLE_API_KEY environment variable gracefully
- [x] Add .env file loading capability (python-dotenv)
- [x] Fix asyncio event loop issue in async calls


## Completed Tasks
- [x] Create agent workflow rule for documentation-driven development
- [x] Fix missing `os` import in main.py
- [x] Fix async main() function call
- [x] Handle missing GOOGLE_API_KEY environment variable gracefully
- [x] Add .env file loading capability (python-dotenv)
- [x] Fix asyncio event loop issue in async calls
- [x] Move code into src folder structure


## Notes
- Project uses pydantic_ai with Google Gemini model
- GOOGLE_API_KEY is configured in .env file
- Code is organized in src/ folder structure
- To run the application:
  - Using script: `collie` (after `uv pip install -e .`)
  - Using module: `PYTHONPATH=src python -m collie.main`
- The app will now provide helpful error messages if the API key is missing
- Application is fully functional and demonstrates:
  - Asynchronous agent call (Italy capital)
  - Asynchronous agent call (France capital)  
  - Streaming agent call (UK capital)
- All asyncio event loop issues have been resolved
