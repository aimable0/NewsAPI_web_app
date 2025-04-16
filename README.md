
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


## 4. Deploying to Web Server

To deploy the app to a production web server, follow these steps:

## Deployment in details
# NewsAroundYou - Deployment Guide

1.  Updated the ubuntu server to match the most recent version..

	check version => lsb_release -a
	update to newer release .. (to make sure our system is uptodate)
		- sudo apt update && sudo apt upgrade && sudo apt dist-upgrade
		-  sudo apt install update-manager-core
		- sudo do-release-upgrade:
			If this “ModuleNotFoundError: No module named 'apt_pkg'” error then:
				- sudo ln -sf /usr/bin/python3.8 /usr/bin/python3 (restore python back to the release 						version default)
				- sudo apt update
				- sudo apt install --reinstall python3-apt
		- sudo reboot (restart)
Or update all packages (if recent version)
	- sudo apt update
	- sudo apt upgrade
	- sudo apt full-upgrade

2.  Sent the app folder using scp to the web server ..
	using scp -r source destination (ex ubuntu@ip:home)
	- mv the folder to the /var/ww/ (or anywhere you want)

  3. Create a virtual environment// from home .. so that you don’t face permission issues when installing stuff with pip.. Started it/ activated within the virtual environment

	=> python3 -m venv venv(environment name)

	if venv is not installed ..:
		- sudo apt install python3-venv -y

	activate the venv (virtual environment)
	source venv\bin\activate

4. Installed requirement libraries + gunicorn
	=> pip install -r [requirements.txt file location]

5. Edited the django app/ settings file to
	1. add the web server in allowed hosts
	2. To add where the static_root location.
		ex: STATIC_ROOT = BASE_DIR / “static/”
	3. Turn the debug off … (maybe if in production)

+ Edit the /etc/systemd/system/gunicorn.socket:

    > paste the following:
—————————start file —————————
	[Unit]
	Description=gunicorn socket

	[Socket]
	ListenStream=/run/gunicorn.sock

	[Install]
	WantedBy=sockets.target
—————————end file —————————

   and gunicorn.service (same location as above)

   > paste the following be sure to check edit your file location..

—————————start file —————————
	[Unit]
	Description=gunicorn daemon
	Requires=gunicorn.socket
	After=network.target

	[Service]
	User=ubuntu
	Group=www-data
	WorkingDirectory=/var/www/app/NewsAPI_web_app (edit this to match yours)
	ExecStart=/home/ubuntu/venv/bin/gunicorn \ (edit this to match yours)
         		   --access-logfile - \
		          --workers 3 \
		          --bind unix:/run/gunicorn.sock \
	        	  NewsAroundYou.wsgi:application (edit this to match yours)

	[Install]
	WantedBy=multi-user.target
—————————end file —————————

+ Start gunicorn service.
	sudo systemctl start gunicorn.socket
	sudo systemctl daemon-reload
	sudo systemctl enable gunicorn.socket

+ Check status
	Checked the gunicorn status (make sure its indicated as active)

+ install nginx (if not installed already)
    - sudo apt update -y
    - sudo apt install nginx

+ Create/edit nginx configuration.file in sites-available to serve the django app

    ex: sudo vi /etc/nginx/sites-available/djangoproject.conf

Sample (paste and edit):
server {
    listen 80;
    server_name web-02.naimable.tech www.naimable.tech (examples);
    add_header X-Served-By $hostname;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/app/NewsAPI_web_app; (should be edited)
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

+ enable the configuration file in sites enabled

	> sudo ln -s /etc/nginx/sites-available/djangoproject.conf /etc/nginx/sites-enabled/
	check if the link is successful:
		sample:
			(venv) ubuntu@6355-web-01:/var/www/app/NewsAPI_web_app$ ls -l /etc/nginx/sites-enabled/
			total 0
			lrwxrwxrwx 1 root root 34 Mar 28 00:20 default -> /etc/nginx/sites-available/default
			lrwxrwxrwx 1 root root 45 Apr 16 00:22 djangoproject.conf -> /etc/nginx/sites-available/				djangoproject.conf

	> check if the configuration in nginx are okey
	comp$ sudo nginx -t
	sample:
		nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
		nginx: configuration file /etc/nginx/nginx.conf test is successful

+ restart nginx
	- systemctl restart nginx
	- systemctl enable nginx

	> check status (if active)
		- systemctl status nginx

	> f any error (in this step) .. allow the nginx in ufw, try:
		- [sudo] ufw allow “Nginx Full”

+ reload daemon
	- sudo systemctl daemon-reload

+ restart gunicorn
	- sudo systemctl restart gunicorn
	- sudo systemctl enable gunicorn

	> check status
		- sudo systemctl status gunicorn
 ≠≠≠≠ test your web server.. example web-01.naimable.tech using a incognito..
	—> you should se the app without css .. (don’t worry we have not yet configured the static files)

+ Create static file folder to render css and other static file
	run the code inside your django project.
	- python3 manage.py collectstatic

+ Test again and  :) this should render the page with its static components.
---

## 5. API Used
- **NewsAPI.org** ([Documentation](https://newsapi.org/docs))

---

## 6. Credits
- **Django** ([Documentation](https://docs.djangoproject.com/en/stable/))
- **Gunicorn** ([Documentation](https://docs.gunicorn.org/en/stable/))
- **Nginx** ([Documentation](https://nginx.org/en/docs/))



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
- [Nginx](https://nginx.org/en/docs/): For the web server that hosts the application.

## Conclusion

This project demonstrates how to integrate external news APIs into a Django web application and how to deploy it to a production environment using Apache. It also highlights the challenges encountered during development and how they were resolved.

