<h1 align="center">Otakusama</h1>

Otakusama is a Manga Reading app made using Flutter for the frontend and Django for the backend. This repository contains the code for the backend part of the app. The frontend repository can be found [here](https://github.com/ilakshaygupt/otakusama-frontend).


<h2 align="center">Key Features</h2>

Otakusama offers essential features for Manga enthusiasts:

- Email (SMTP) for Signup/Signin.
- Two-Factor Authentication (2FA) with Enable/Disable through Phone Number .
- JWT Authentication with Refresh and Access tokens.
- Real-time Data through Web Scraping.
- Celery and Celerybeat for background tasking such as Sending Emails, SMS.
- Deployment on AWS EC2 instance.
- Dockerized all the services (Backend, Celery, Celerybeat, Redis and  PostgreSQL ).


<h2 align="center">PREVIEW</h2>

<p align="center">
  <img src="https://github.com/ilakshaygupt/otakusama-backend/assets/99826011/60276f73-6802-450d-a9dd-5fe6439eee1a" width="200" />  
</p>

<p align="center">
  <img src="https://github.com/ilakshaygupt/otakusama-backend/assets/99826011/e13796da-40a2-480a-8e06-7ca2e7579f2b" width="150" />
  <img src="https://github.com/ilakshaygupt/otakusama-backend/assets/99826011/d9eb1a01-84d8-4947-a302-39f48555c9e7" width="150" />
  <img src="https://github.com/ilakshaygupt/otakusama-backend/assets/99826011/a4674d82-f3f4-4c8c-800e-aecc51072da0" width="150" />
  <img src="https://github.com/ilakshaygupt/otakusama-backend/assets/99826011/9e97f153-bdfc-46b1-809c-6c6cb87f5601" width="150" />
</p>



<h2 align="center">Running Otakusama with Docker Compose</h2>

Follow these steps to set up and run Otakusama using Docker Compose:

**Prerequisites:**

- Make sure you have Docker and Docker Compose installed on your machine. If not, you can [install them here](https://docs.docker.com/compose/install/).

**1. Clone the Repository:**

Clone the Otakusama repository to your local machine using the following command:

```bash
git clone https://github.com/ilakshaygupt/otakusama-backend
```

**2. Navigate to the project directory:**

```bash
cd otakusama-backend
```

**3. Configure the Environment Variables:**

Edit the docker.env file located in the project's root directory to customize the environment variables to your specific requirements.

**4. Start the Containers:**

Build and start the Docker containers using the following command:

```bash
docker-compose up --build
```

This command will pull necessary images, build all the services, and start the containers.

**5. Access the Otakusama Web:**

Once the containers are up and running, you can access the Otakusama application in your web browser using the following URLs:

- **Backend:** [http://localhost:8000](http://localhost:8000)



**Troubleshooting:**

./entrypoint.sh not found

- Open the `entrypoint.sh` file in a text editor.
- Change the line ending sequence to LF (Line Feed). You can usually do this by configuring your text editor to save the file with LF line endings.
- Save the changes to the `entrypoint.sh` file.
- Rebuild the containers using the `docker-compose up --build` command.

./entrypoint.sh: permission denied

- Grant execute permissions to the `entrypoint.sh` file using the following command:

```bash
sudo chmod +x entrypoint.sh
```

<h2 align="center">Setting Up Otakusama on a Local Server</h2>

Follow these steps to set up Otakusama on your local server:

**Prerequisites:**

1. **Python:** Make sure you have Python installed on your machine. If not, you can [install it here](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/).

2. **PostgreSQL:** Make sure you have PostgreSQL installed on your machine. If not, you can [install it here](https://www.postgresql.org/download/).

3. **Redis:** Make sure you have Redis installed on your machine. If not, you can [install it here](https://redis.io/download).

**Getting Started:**

**1. Clone the Repository:**

Clone the Otakusama repository to your local machine using the following command:

```bash
git clone https://github.com/ilakshaygupt/otakusama-backend
```

**2. Navigate to the project directory:**

```bash
cd otakusama-backend
```

**3. Create and Activate a Virtual Environment:**

```bash
pip install virtualenv
virtualenv venv
venv/scripts/activate  # On Windows
source venv/bin/activate  # On Linux and macOS
```

**4. Install the Dependencies:**

```bash
pip install -r requirements.txt
```

**5. Configure the Environment Variables:**

Create a .env file in the otakusma-backend/otakusma-backend directory and add the following environment variables to it:

```env
EMAIL_BACKEND=
EMAIL_HOST=
EMAIL_USE_TLS=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
API_KEY=
GOOGLE_CLIENT_ID=
SOCIAL_AUTH_PASSWORD=
GOOGLE_CLIENT_SECRET=
SECRET_KEY =
```

**6. Create the Database:**

Create a PostgreSQL database and connect to it by entering credentials in .env file, once connected run the migrate command:

```bash
python manage.py migrate
```

**7. Create a Superuser:**

**You can create a superuser account executing the following commands:**

```bash
python manage.py createsuperuer
```

A prompt will appear asking for email followed by password.

**Alternatively, you can create a superuser by using the following custom command:**

```bash
python manage.py add_superuser --email <email> --password <password>
```

**8. Run the Backend Server:**

```bash
python manage.py runserver
```

**Access the endpoints in your web browaer:** [http://localhost:8000](http://localhost:8000)

**Access the Django Admin Panel, go to:** [http://localhost:8000/admin](http://localhost:8000/admin)

Use the superuser credentials to login.


These steps will get you up and running with the Otakusama backend on your local machine.


<div align="center">
  <h2>Frontend Repository</h2>
  <h4><a href="https://github.com/ilakshaygupt/otakusama-backend">Otakusama Backend</a></h4>
</div>
