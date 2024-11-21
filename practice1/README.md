practice1/
├── main.py             # Application logic with endpoints.
├── semi1.py            # All code and functions of seminar 1
├── Dockerfile          # Docker image setup.
├── docker-compose.yml  # Docker Compose configuration.
├── requirements.txt    # Python dependencies.
└── README.md           # Documentation.


1. First, we create an API following the instructions in https://fastapi.tiangolo.com/
We make sure it's running using this command: fastapi dev main.py
This is the output:

(base) viktoriaolmedo@poblenou-132-162 practice1 % fastapi dev main.py
INFO     Using path main.py                                                     
INFO     Resolved absolute path /Users/viktoriaolmedo/practice1/main.py         
INFO     Searching for package file structure from directories with __init__.py 
         files                                                                  
INFO     Importing from /Users/viktoriaolmedo/practice1                         
                                                                                
 ╭─ Python module file ─╮                                                       
 │                      │                                                       
 │  🐍 main.py          │                                                       
 │                      │                                                       
 ╰──────────────────────╯                                                       
                                                                                
INFO     Importing module main                                                  
[1, 0, 3, 65, 3, 66, 2, 67, 1, 68, 2, 65]
INFO     Found importable FastAPI app                                           
                                                                                
 ╭─ Importable FastAPI app ─╮                                                   
 │                          │                                                   
 │  from main import app    │                                                   
 │                          │                                                   
 ╰──────────────────────────╯                                                   
                                                                                
INFO     Using import string main:app                                           
                                                                                
 ╭────────── FastAPI CLI - Development mode ───────────╮                        
 │                                                     │                        
 │  Serving at: http://127.0.0.1:8000                  │                        
 │                                                     │                        
 │  API docs: http://127.0.0.1:8000/docs               │                        
 │                                                     │                        
 │  Running in development mode, for production use:   │                        
 │                                                     │                        
 │  fastapi run                                        │                        
 │                                                     │                        
 ╰─────────────────────────────────────────────────────╯                        
                                                                                
INFO:     Will watch for changes in these directories: ['/Users/viktoriaolmedo/practice1']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [17073] using WatchFiles
[1, 0, 3, 65, 3, 66, 2, 67, 1, 68, 2, 65]
INFO:     Started server process [17075]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


This is how we know the FastAPI is running.
Then we need to put it inside a docker. For that, we create a Dockerfile with all the dependencies and run the Docker container using the image.
