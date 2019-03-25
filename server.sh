source activate py2
sudo apt-get install python-dev default-libmysqlclient-dev
sudo apt-get install libmysqlclient-dev
pip install Flask
export FLASK_APP=index.py
export FLASK_DEBUG=0
flask run --host=0.0.0.0
