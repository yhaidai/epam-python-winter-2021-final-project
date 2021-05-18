let ADD_DEPARTMENT_SELECT_ID = "#add-select-department";
let EDIT_DEPARTMENT_SELECT_ID = "#edit-select-department";
let EDIT_CHANGE_DEPARTMENT_SELECT_ID = "#edit-change-department";
let DELETE_DEPARTMENT_SELECT_ID = "#delete-select-department";

let EDIT_EMPLOYEE_SELECT_ID = "#edit-select-employee";
let DELETE_EMPLOYEE_SELECT_ID = "#delete-select-employee";

let ADD_NAME_ID = "#add-name";
let ADD_DATE_OF_BIRTH_ID = "#add-dob";
let ADD_SALARY_ID = "#add-salary";
let EDIT_NAME_ID = "#edit-name";
let EDIT_DATE_OF_BIRTH_ID = "#edit-dob";
let EDIT_SALARY_ID = "#edit-salary";

let ADD_EMPLOYEE_FORM_ID = "#add-employee-form";
let EDIT_EMPLOYEE_FORM_ID = "#edit-employee-form";
let DELETE_EMPLOYEE_FORM_ID = "#delete-employee-form";


$(document).ready(function () {
    fetch("/api/departments")
        .then((response) => response.json())
        .then((departments) => {
            initForms(departments)
        })
        .catch((err) => {
            console.log(err);
        });
});

function initForms(departments) {
    initAddEmployeeForm(departments);
    initEditEmployeeForm(departments);
    initDeleteEmployeeForm(departments);
}

function initAddEmployeeForm(departments) {
    initDepartmentSelect(ADD_DEPARTMENT_SELECT_ID, departments);

    $(ADD_EMPLOYEE_FORM_ID).submit(function (event) {
        let data = {
            name: $(ADD_NAME_ID).val(),
            date_of_birth: $(ADD_DATE_OF_BIRTH_ID).val(),
            salary: $(ADD_SALARY_ID).val(),
            department: {
                uuid: $(ADD_DEPARTMENT_SELECT_ID + " option:selected").val()
            }
        }

        fetchWithAlert(
            `/api/employees/`,
            "POST",
            "Successfully added employee",
            "Failed to add employee",
            data
        )
    });
}

function initEditEmployeeForm(departments) {
    initDepartmentSelect(EDIT_DEPARTMENT_SELECT_ID, departments);
    initDepartmentSelect(EDIT_CHANGE_DEPARTMENT_SELECT_ID, departments);

    let department = getSelectedDepartment(EDIT_DEPARTMENT_SELECT_ID, departments)
    initEmployeeSelect(EDIT_EMPLOYEE_SELECT_ID, department.employees);

    initEmployeeInputs(
        EDIT_DEPARTMENT_SELECT_ID, EDIT_EMPLOYEE_SELECT_ID, EDIT_NAME_ID,
        EDIT_DATE_OF_BIRTH_ID, EDIT_SALARY_ID, EDIT_CHANGE_DEPARTMENT_SELECT_ID
    );

    // reinitialise employee select on department option change
    $(EDIT_DEPARTMENT_SELECT_ID).change(function () {
        let department = getSelectedDepartment(EDIT_DEPARTMENT_SELECT_ID, departments)
        initEmployeeSelect(EDIT_EMPLOYEE_SELECT_ID, department.employees);
    });

    // reinitialise employee inputs on employee option change
    $(EDIT_EMPLOYEE_SELECT_ID).change(function () {
        initEmployeeInputs(
            EDIT_DEPARTMENT_SELECT_ID, EDIT_EMPLOYEE_SELECT_ID, EDIT_NAME_ID,
            EDIT_DATE_OF_BIRTH_ID, EDIT_SALARY_ID, EDIT_CHANGE_DEPARTMENT_SELECT_ID
        );
    });

    $(EDIT_EMPLOYEE_FORM_ID).submit(function (event) {
        let uuid = $(`${EDIT_EMPLOYEE_SELECT_ID} option:selected`).val();
        let data = {
            name: $(EDIT_NAME_ID).val(),
            date_of_birth: $(EDIT_DATE_OF_BIRTH_ID).val(),
            salary: $(EDIT_SALARY_ID).val(),
            department: {
                uuid: $(EDIT_CHANGE_DEPARTMENT_SELECT_ID + " option:selected").val()
            }
        }

        fetchWithAlert(
            `/api/employee/${uuid}`,
            "PUT",
            "Successfully edited employee",
            "Failed to edit employee",
            data
        )
    });
}

function initDeleteEmployeeForm(departments) {
    initDepartmentSelect(DELETE_DEPARTMENT_SELECT_ID, departments);

    let department = getSelectedDepartment(DELETE_DEPARTMENT_SELECT_ID, departments)
    initEmployeeSelect(DELETE_EMPLOYEE_SELECT_ID, department.employees);

    // reinitialise employee select on department option change
    $(DELETE_DEPARTMENT_SELECT_ID).change(function () {
        let department = getSelectedDepartment(DELETE_DEPARTMENT_SELECT_ID, departments)
        initEmployeeSelect(DELETE_EMPLOYEE_SELECT_ID, department.employees);
    });

    $(DELETE_EMPLOYEE_FORM_ID).submit(function (event) {
        let uuid = $(`${DELETE_EMPLOYEE_SELECT_ID} option:selected`).val();

        fetchWithAlert(
            `/api/employee/${uuid}`,
            "DELETE",
            "Successfully deleted employee",
            "Failed to delete employee"
        )
    });
}

function initDepartmentSelect(departmentSelectId, departments) {
    let url = (" " + window.location).slice(1)
    let urlSuffix = url.replace(window.origin, "")
    let urlParts = urlSuffix.split("/").filter(Boolean)
    let expanded = urlParts[1]
    let departmentSelectElement = $(departmentSelectId)

    // initialize options
    departments.forEach(department => {
        departmentSelectElement.append(
            `<option value="${department.uuid}">
                ${department.name} (${department.organisation})
            </option>`
        )
    });

    // select initial department and employee options
    if (departmentSelectId.includes(expanded) && expanded !== "add") {
        let employeeUUID = urlParts[2].split('?')[0]
        let department = getDepartmentByEmployeeUUID(employeeUUID, departments)
        if (departments.length) {
            if (!department) {
                department = departments[0]
            }
            departmentSelectElement.val(department.uuid)
        }
    }
}

function getDepartmentByEmployeeUUID(employeeUUID, departments) {
    let result = undefined
    departments.forEach(department => {
        let employees = department.employees.filter(
            (employee) => employee.uuid === employeeUUID
        );
        if (employees.length) {
            result = department;
        }
    });

    return result;
}

function getSelectedDepartment(departmentSelectId, departments) {
    let departmentUUID = $(`${departmentSelectId} option:selected`).val()
    return departments.filter(department => department.uuid === departmentUUID)[0]
}

function initEmployeeSelect(employeeSelectId, employees) {
    let url = (" " + window.location).slice(1)
    let urlSuffix = url.replace(window.origin, "")
    let urlParts = urlSuffix.split("/").filter(Boolean)
    let expanded = urlParts[1]
    let employeeSelectElement = $(employeeSelectId)

    // initialize options
    employeeSelectElement.empty()
    employees.forEach(employee => {
        employeeSelectElement.append(
            `<option value="${employee.uuid}">
                ${employee.name} (${employee.date_of_birth} ${employee.salary}$)
            </option>`
        )
    });

    // select initial department and employee options
    if (employeeSelectId.includes(expanded) && expanded !== "add") {
        let employeeUUID = urlParts[2]
        employeeSelectElement.val(employeeUUID)
    }

    // if select element is empty initialise it with first employee
    if (employees.length && !employeeSelectElement.val()) {
        employeeSelectElement.val(employees[0].uuid)
    }
    employeeSelectElement.change()
}

function initEmployeeInputs(departmentSelectId, employeeSelectId, nameInputId,
                            dateOfBirthInputId, salaryInputId, departmentChangeId) {
    let department = $(`${departmentSelectId} option:selected`).val();
    let employee = $(`${employeeSelectId} option:selected`).text();
    let employeeRegexp = /(.*?)(?= \((\d{4}-\d{2}-\d{2}) (\d+)\$\))/;
    let match = employeeRegexp.exec(employee);
    let name = match[0].trim();
    let dateOfBirth = match[2].trim();
    let salary = match[3].trim();

    $(nameInputId).val(name);
    $(dateOfBirthInputId).val(dateOfBirth);
    $(salaryInputId).val(salary);
    $(departmentChangeId).val(department);
}

function fetchWithAlert(url, method, successMessage, failureMessage, data = {}) {
    fetch(url, {
        method: method,
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(checkStatus)
        .then((response) => {
            if (response.status === 204) {
                return response;
            }
            return response.json()
        })
        .then((department) => {
            alert(successMessage);
        })
        .catch((err) => {
            console.log(err);
            alert(failureMessage, false);
        });
}

function checkStatus(response) {
    if (response.ok) {
        return Promise.resolve(response);
    } else {
        return Promise.reject(new Error(response.statusText));
    }
}

function alert(message, success = true) {
    let cls = 'alert-success'
    if (!success) {
        cls = 'alert-danger'
    }

    $("body").prepend(
        `<div class="alert ${cls} alert-dismissible fade in text-center">
            <a href="#" class="close" data-dismiss="alert" 
            aria-label="close">&times;</a>
            <strong>${message}</strong>
        </div>`
    )
    setTimeout(() => {
        $(`.${cls}`).last().remove()
    }, 10000);
}
