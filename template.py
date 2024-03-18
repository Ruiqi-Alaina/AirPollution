import os
from pathlib import Path
import logging

# logging str
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    "src/__init__.py",
    "src/components/__init__.py",
    "src/utils/__init__.py",
    "src/config/__init__.py",
    "src/config/configuration.py",
    "src/pipeline/__init__.py",
    "src/entity/__init__.py",
    "src/constants/__init__.py",
    "requirements.txt",
    "setup.py",
]

for file_path in list_of_files:
    file_path =  Path(file_path)
    filedir, filename = os.path.split(file_path)
    
    if filedir !="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"The directory {filedir} has been created" )
        
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
            with open(file_path, 'w') as file:
                pass    
    else:
        logging.info(f"The file {file_path} already exists")
    
            
        


