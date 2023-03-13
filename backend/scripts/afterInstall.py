print("after")
import os

os.system('sudo chmod -R gu+rwx /home/ubuntu/backend')

os.system('python3 -m venv /home/ubuntu/backend/venv')
os.system('sudo chown -R ubuntu.ubuntu /home/ubuntu/backend')
os.system('sudo chmod -R gu+rwx /home/ubuntu/backend')
os.system(
    '. /home/ubuntu/backend/venv/bin/activate && pip install --upgrade pip && pip install -r /home/ubuntu/backend/requirements/prod.txt && python /home/ubuntu/backend/manage.py migrate --settings=mysite.settings.product')
os.system('python /home/ubuntu/backend/manage.py --no-input')
os.system('sudo systemctl restart mysite.service')
os.system('sudo systemctl restart nginx')

    
