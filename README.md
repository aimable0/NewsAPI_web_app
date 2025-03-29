
# News Around You - Django Web Application

This web application allows users to search and navigate through different categories of news headlines, such as Business, Health, Sports, Technology, and more. The app uses the [NewsAPI](https://newsapi.org) to fetch live news data and display it to the user.

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

```apache
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/your-django-app

    WSGIDaemonProcess your-django-app python-path=/var/www/your-django-app python-home=/var/www/your-django-app/djangoenv
    WSGIProcessGroup your-django-app
    WSGIScriptAlias / /var/www/your-django-app/your_django_app/wsgi.py

    <Directory /var/www/your-django-app/your_django_app>
        Require all granted
    </Directory>
</VirtualHost>
```

4. Restart Apache to apply the configuration:

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

## Link to Demo
