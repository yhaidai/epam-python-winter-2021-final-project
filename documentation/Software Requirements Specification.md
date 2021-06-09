# <p style="text-align: center;"> Department App </p>

### Vision

Department App is a web application which allows users to record information 
about departments and employees.

Application should provide:
- Storing departments and employees in database
- Display list of departments
- Managing the list of departments (adding, editing, removing)
- Display list of employees
- Managing the list of employees (adding, editing, removing)
- Searching employees by date of birth
- Searching employees born in specified period

### 1. Homepage

***Main scenario:***
- User selects *"Home"* menu item
- Application homepage is displayed (Pic 1.1)

<figure class="image">
  <img src="../department_app/static/images/homepage.png" alt="Homepage" 
style="display: block">
  <figcaption>Pic 1.1 Navigation to the "Browse departments" option</figcaption>
</figure>

### 2. Departments

#### 2.1 Display list of departments

The mode is designed to view the list of departments.

***Main scenario:***
- User selects submenu item *"Browse departments"* at the *"Departments"* 
  menu (Pic 2.1)
- Application displays list of departments (Pic 2.2)

<figure class="image">
  <img src="../department_app/static/images/browse_departments_navigation.
png" alt="Navigation to the 'Browse departments' option" style="display: block">
  <figcaption>Pic 2.1 Navigation to the "Browse departments" option</figcaption>
</figure>

<figure class="image">
  <img src="../department_app/static/images/browse_departments_page.png" 
alt="'Browse departments' page" style="display: block">
  <figcaption>Pic 2.2 List of departments</figcaption>
</figure>

The list displays the following columns:
- \# - number of the department in the list
- Department - name of the department
- Organisation - organisation the department belongs to
- Average salary - average salary across all the employees that works in the department

#### 2.2 Add department

***Main scenario:***
- User clicks the *"Add department"* button in the departments list view mode
- Application redirects user to the department management page with the "Add 
  department" panel being active
- User enters data and presses the *"Submit"* button
- If entered data is valid, the record is added to the database and message 
  indicating success is displayed
- If error occurs, then error message is displayed

<figure class="image">
  <img src="../department_app/static/images/add_department.png" 
alt="'Add department' view" style="display: block">
  <figcaption>Pic 2.3 Adding a department</figcaption>
</figure>

When adding a department the following details are entered:
- Department name - name of the department
- Department organisation - organisation the department belongs to

Constraints for data validation:
- Department name and organisation must be unique i.e., no other department 
  with such name and organisation can exist

#### 2.3 Edit department

***Main scenario:***
- User clicks the *"Edit"* button in the departments list view mode
- Application redirects user to the department management page with the "Edit 
  department" panel being active
- User chooses the department, enters data and presses the *"Submit"* button
- If entered data is valid, the corresponding record is updated in the database 
  and message indicating success is displayed
- If error occurs, then error message is displayed

<figure class="image">
  <img src="../department_app/static/images/edit_department.png" 
alt="'Edit department' view" style="display: block">
  <figcaption>Pic 2.4 Editing a department</figcaption>
</figure>

When editing a department the following details are entered:
- Department name - name of the department
- Department organisation - organisation the department belongs to

Constraints for data validation:
- Department name and organisation must be unique i.e., no other department 
  with such name and organisation can exist

#### 2.4 Delete department

***Main scenario:***
- User clicks the *"Delete"* button in the departments list view mode
- Application redirects user to the department management page with the "Delete 
  department" panel being active
- User chooses the department and presses the *"Delete"* button
- If chosen department is still in the database, the corresponding record is 
  deleted from the database and message indicating success is displayed
- If error occurs, then error message is displayed

<figure class="image">
  <img src="../department_app/static/images/delete_department.png" 
alt="'Delete department' view" style="display: block">
  <figcaption>Pic 2.5 Deleting a department</figcaption>
</figure>


### 3. Employees