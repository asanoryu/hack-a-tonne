<b>Flaskbarebones</b>

Installation:
    
    pip3 install -r requirements.txt

    Linux:
    sudo -s
    export FLASK_APP=flask_barebones.py

    Windows
    set FLASK_APP=flask_barebones.py

Database setup:
    
    flask db upgrade

Run:

    flask run


Generate new DB migrations:

     flask db migrate -m"migration name"
