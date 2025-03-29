
# News Around You - Django Web Application

This web application allows users to search and navigate through different categories of news headlines, such as Business, Health, Sports, Technology, and more. The app uses the [NewsAPI](https://newsapi.org) to fetch live top news data and display it to the user.

## Link to Demo
https://youtu.be/gB-2hEPr728

## Uniquiness of the application
This application fetches for the user from most trusted sources the top headlines of what's happening around him/her so that they can be updated on what's going on.

## Key Features

- Users can view headlines from different categories like Business, Technology, Health, etc.
- Allows searching for specific news articles, or keyword.
- Handles ratelimits and errors
- Fetches news from the [NewsAPI](https://newsapi.org).
- Built using Django with HTML and CSS for the front end.

## Requirements

Ensure you have the following dependencies installed:

- Python 3.12 (or higher)
- Django 5.1.7
- Python-dotenv (for environment variables)
- requests (for API calls)
- rich (for rich output)
- Other dependencies as listed below.

### Dependencies
- asgiref==3.8.1
- certifi==2025.1.31
- charset-normalizer==3.4.1
- Django==5.1.7
- idna==3.10
- markdown-it-py==3.0.0
- mdurl==0.1.2
- printjson==1.0.1
- Pygments==2.19.1
- python-dotenv==1.1.0
- requests==2.32.3
- rich==13.9.4
- sqlparse==0.5.3
- urllib3==2.3.0

## Setup Instructions

### 1. Install Dependencies

First, clone the repository and navigate to the project directory:

```bash
git clone https://github.com/aimable0/NewsAPI_web_app.git
cd NewsAroundYou
```

Then, create a virtual environment and activate it:

```bash
python3 -m venv djangoenv
source djangoenv/bin/activate  # For Linux/MacOS
djangoenv\Scriptsctivate.bat  # For Windows
```

Next, install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory and add your API key from [NewsAPI](https://newsapi.org). For example:

```
NEWS_API_KEY=your_api_key_here
```

### 3. Run the Application Locally

After setting up your environment, run the following command to start the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to see the app in action.


## Deploying to Web Server

To deploy the app to a production web server, follow these steps:

1. Install Apache and mod_wsgi:

```bash
sudo apt install apache2 libapache2-mod-wsgi-py3
```

2. Set up your Django project on the server, typically in `/var/www/`.

3. Configure your Apache virtual host to serve the Django application. Ensure you include a WSGI configuration like:

4. Restart Apache to apply the configuration:


## Deployment in details
# NewsAroundYou - Deployment Guide

## Prerequisites
Before starting the deployment, ensure that you have the following:
- Ubuntu server (16 or later)
- Python 3.12 installed
- Apache2 and uWSGI installed
- Git installed on the server

---

## 1. Setting Up the Server

### Updating and Installing Dependencies
```sh
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3.12 python3.12-dev python3-venv python3-pip gcc -y
sudo apt-get install apache2 libapache2-mod-wsgi-py3 uwsgi uwsgi-plugin-python3 -y
sudo apt-get install ufw nginx -y
```

### Configuring Firewall
```sh
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

---

## 2. Setting Up Git and Cloning the Application
### Installing Git on the Server
```sh
sudo apt-get install git -y
```

### Cloning the Application
```sh
cd /var/www
sudo git clone https://github.com/yourusername/NewsAroundYou.git
cd NewsAroundYou
```

---

## 3. Creating and Configuring Virtual Environment
```sh
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

Ensure proper permissions:
```sh
sudo chown -R $USER:$USER /var/www/NewsAroundYou/venv
```

---

## 4. Configuring Django
### Updating Django Settings
Edit `settings.py`:
```python
ALLOWED_HOSTS = ['your-server-ip', 'yourdomain.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```
Run migrations and collect static files:
```sh
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 5. Configuring uWSGI
### Creating the uWSGI Configuration File
Create `/var/www/NewsAroundYou/uwsgi.ini`:
```ini
[uwsgi]
chdir = /var/www/NewsAroundYou
module = NewsAroundYou.wsgi:application
home = /var/www/NewsAroundYou/venv
socket = /var/www/NewsAroundYou/NewsAroundYou.sock
chmod-socket = 664
vacuum = true
master = true
processes = 4
```

### Running uWSGI
```sh
uwsgi --ini /var/www/NewsAroundYou/uwsgi.ini
```

---

## 6. Configuring Apache
### Creating an Apache Configuration File
Create `/etc/apache2/sites-available/newsaroundyou.conf`:
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com

    DocumentRoot /var/www/NewsAroundYou

    <Directory /var/www/NewsAroundYou>
        Require all granted
    </Directory>

    Alias /static /var/www/NewsAroundYou/static
    <Directory /var/www/NewsAroundYou/static>
        Require all granted
    </Directory>

    WSGIDaemonProcess NewsAroundYou python-home=/var/www/NewsAroundYou/venv python-path=/var/www/NewsAroundYou
    WSGIProcessGroup NewsAroundYou
    WSGIScriptAlias / /var/www/NewsAroundYou/NewsAroundYou/wsgi.py
</VirtualHost>
```
Enable the site and restart Apache:
```sh
sudo a2ensite newsaroundyou.conf
sudo systemctl restart apache2
```

---

## 7. Configuring Nginx as a Load Balancer (Optional)
### Creating an Nginx Configuration File
Create `/etc/nginx/sites-available/newsaroundyou`:
```nginx
upstream app_servers {
    server 192.168.1.10:8000;
    server 192.168.1.11:8000;
}
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Enable the site and restart Nginx:
```sh
sudo ln -s /etc/nginx/sites-available/newsaroundyou /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 8. Testing the Deployment
### Verify Application Running
```sh
curl http://your-server-ip
```
### Verify uWSGI Socket
```sh
ls -lah /var/www/NewsAroundYou/NewsAroundYou.sock
```
### Check Logs for Issues
```sh
sudo tail -f /var/log/apache2/error.log
sudo tail -f /var/log/nginx/error.log
```

---

## 9. Challenges Faced and Solutions
### Working with Virtual Environments
**Issue:** `pip install` failing due to permissions
**Solution:** Ensure virtual environment has correct ownership:
```sh
sudo chown -R $USER:$USER /var/www/NewsAroundYou/venv
```

### Fixing uWSGI Module Errors
**Issue:** `uwsgi --module` throwing an invalid option error
**Solution:** Install uWSGI plugins:
```sh
sudo apt install uwsgi uwsgi-plugin-python3
```


---

## 10. API Used
- **NewsAPI.org** ([Documentation](https://newsapi.org/docs))

---

## 11. Credits
- **Django** ([Documentation](https://docs.djangoproject.com/en/stable/))
- **uWSGI** ([Documentation](https://uwsgi-docs.readthedocs.io/en/latest/))
- **Apache** ([Documentation](https://httpd.apache.org/docs/))



```bash
sudo systemctl restart apache2
```

## API Documentation

This app uses the [NewsAPI](https://newsapi.org) to fetch news data. Please refer to their official documentation for detailed usage instructions and API limits.

## Challenges

- **Deployment issues with Apache**: One of the main challenges was ensuring that Apache served the Django application correctly using mod_wsgi. After configuring the Apache virtual host and ensuring all file paths were set correctly, the application began serving as expected.
- **Static files handling**: Another challenge was configuring static files in Django when deployed to the web server. I had to ensure that Apache was configured to serve these files.

## Credits

- [NewsAPI](https://newsapi.org): For providing live news data.
- [Django](https://www.djangoproject.com/): For the framework used to build this web application.
- [Apache](https://httpd.apache.org/): For the web server that hosts the application.

## Conclusion

This project demonstrates how to integrate external news APIs into a Django web application and how to deploy it to a production environment using Apache. It also highlights the challenges encountered during development and how they were resolved.

