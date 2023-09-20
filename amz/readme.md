# README

pre-requisites:

type below command in terminal

```bash
git --version
python --version or python3 --version
geckodriver --version
```
##### Create project folder:

open terminal

```bash
mkdir work
cd work
git clone https://github.com/grootzz26/web_scraping.git
cd web_scraping
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Open Browser

[link](http://127.0.0.1:8000/home/)




