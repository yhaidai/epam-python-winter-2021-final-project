# EPAM Online UA Winter 2021 final project - Department App


## With this app you can:
- ### Display a list of departments and the average salary (calculated automatically) for these departments
  
- ### Display a list of employees in the departments with an indication of the salary for each employee and a search field to search for employees born on a certain date or in the period between dates

- ### Change (add / edit / delete) the above data


## How to build this project:

- ### Navigate to the project root folder

- ### Optionally set up and activate the virtual environment:
```
virtualenv venv
source env/bin/activate
```

- ### Install the requirements:
```
pip install -r requirements.txt
```
- ### Configure MySQL database

- ### Set the following environment variables:

```
MYSQL_USER=<your_mysql_user>
MYSQL_PASSWORD=<your_mysql_user_password>
MYSQL_SERVER=<your_mysql_server>
MYSQL_DATABASE=<your_mysql_database_name>
```

*You can set these in .env file as the project uses dotenv module to load 
environment variables*

- ### Run migrations to create database infrastructure:
```
flask db upgrade
```

- ### Optionally populate the database with sample data
```
python -m department_app/database/populate.py
```

- ### Run the project locally:
```
python -m flask run
```

## Now you should be able to access the web service and web application on the following addresses:

- ### Web Service:
```
localhost:5000/api/departments
localhost:5000/api/department/<uuid>

localhost:5000/api/employees
localhost:5000/api/employees/search/date=<YYYY-MM-DD>
localhost:5000/api/employees/search/start_date=<YYYY-MM-DD>&end_date=<YYYY-MM-DD>
localhost:5000/api/employee/<uuid>
```

#### Web Service endpoints are documented with SwaggerUI at:
```
localhost:5000/swagger
```

- ### Web Application:
```
localhost:5000/

localhost:5000/departments
localhost:5000/department/add
localhost:5000/department/edit
localhost:5000/department/edit/<uuid>
localhost:5000/department/delete
localhost:5000/department/delete/<uuid>

localhost:5000/employees
localhost:5000/employee/add
localhost:5000/employee/edit
localhost:5000/employee/edit/<uuid>
localhost:5000/employee/delete
localhost:5000/employee/delete/<uuid>
```
