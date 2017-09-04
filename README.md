Install Virtual Environment if not:

sudo apt-get install virtualenv

Create a virtual environment with python3 :

virtualenv -p python3 venv

Activate virtual environment :

source venv/bin/activate

Install Git if not :

sudo apt-get install git

Initialised Git :

git init

Clone the Repository: 

git clone https://github.com/ashutosh-007/innov8-assignment.git

Install python3-pip:

sudo apt-get install python3-pip

Install requirements:

pip3 install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

go to http://localhost:8000/home/
