# Honours-Project
## Running the project:

1. Clone main branch:

```
git clone https://github.com/amclau303/Honours-Project
```

2. Have most up to date version of Python installed

3. Navigate to the library. Open a terminal and use the command:

```
pip install virtualenv
```

4. Once the library has been installed, create virtual environment:

```
virtualenv venv
```

5. You can activate this virtual environment using the following command in a cmd prompt:
```
venv\Scripts\activate
```

If you are using Windows Powershell, use the command:
```
venv/Scripts/activate
```

Running this command in an admin powershell prompt should allow this to work if running scripts is disabled on your system:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

6. Once you are inside the virual environment, install all required dependencies:

```
pip install -r requirements.txt
```

7. If it is the first time running this project inside the virtual environment use the following commands:

```
py manage.py makemigrations
```
```
py manage.py migrate
```

8. To run the application, use the following command:

```
py manage.py runserver
```

9. To view the website, the link will be provided in the command prompt via Django


If a new library has been added to the project, while using an active virtual environment, use the following command to update your requirements.txt file, and push it to the repo:

```
pip freeze --local > requirements.txt
```
