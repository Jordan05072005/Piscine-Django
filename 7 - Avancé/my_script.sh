sudo apt update
sudo apt install python3-venv gettext postgresql postgresql-contrib
python3 -m venv django_venv
source django_venv/bin/activate
pip install -r requirements.txt