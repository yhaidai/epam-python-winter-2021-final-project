let EDIT_EMPLOYEE_URL = "#edit-employee-url";
let DELETE_EMPLOYEE_URL = "#delete-employee-url";
let EMPLOYEE_TABLE_ID = "#employees-table";
let SEARCH_EMPLOYEE_TOGGLE_CHECKBOX_ID = "#search-toggle-checkbox";
let SEARCH_BY_DOB_FORM_ID = "#search-by-dob-form";
let SEARCH_BY_DOB_PERIOD_FORM_ID = "#search-by-dob-period-form";
let DATE_INPUT_INPUT_ID = "#date";
let START_DATE_INPUT_ID = "#start-date";
let END_DATE_INPUT_ID = "#end-date";

let EMPLOYEE_API_URL = '/api/employees';


$(document).ready(function () {
    if (!window.location.href.includes("?#")) {
        window.location += "?#"
    }

    initEmployeesTableFromUrl(EMPLOYEE_API_URL);
    initSearchToggleCheckbox();
    initSearchByDateButton();
    initSearchByPeriodButton();
});

function initSearchToggleCheckbox() {
    let searchByDateForm = $(SEARCH_BY_DOB_FORM_ID);
    let searchByPeriodForm = $(SEARCH_BY_DOB_PERIOD_FORM_ID);

    $(SEARCH_EMPLOYEE_TOGGLE_CHECKBOX_ID).click(function () {
        searchByDateForm.toggleClass('hidden');
        searchByPeriodForm.toggleClass('hidden');
    });
}

function initSearchByDateButton() {
    $(SEARCH_BY_DOB_FORM_ID).submit(function () {
        let date = $(DATE_INPUT_INPUT_ID).val();
        let url = `/api/employees/search?date=${date}`;

        initEmployeesTableFromUrl(url);
    });
}

function initSearchByPeriodButton() {
    $(SEARCH_BY_DOB_PERIOD_FORM_ID).submit(function () {
        let startDate = $(START_DATE_INPUT_ID).val();
        let endDate = $(END_DATE_INPUT_ID).val();
        let url = `/api/employees/search?start_date=${startDate}&end_date=${endDate}`;

        initEmployeesTableFromUrl(url);
    });
}

function initEmployeesTableFromUrl(url) {
    fetch(url)
        .then((response) => response.json())
        .then((employees) => {
            initEmployeesTable(employees);
        })
        .catch((err) => {
            if (url !== EMPLOYEE_API_URL) {
                initEmployeesTableFromUrl(EMPLOYEE_API_URL)
            }
            console.log(err);
        });
}

function initEmployeesTable(employees) {
    let edit_employee_base_url = $(EDIT_EMPLOYEE_URL).data().url;
    let delete_employee_base_url = $(DELETE_EMPLOYEE_URL).data().url;
    let employeeTableBody = $(`${EMPLOYEE_TABLE_ID} tbody`)

    employeeTableBody.empty()
    for (let i = 0; i < employees.length; i++) {
        let employee = employees[i];
        let edit_employee_url = `${edit_employee_base_url}/${employee.uuid}`;
        let delete_employee_url = `${delete_employee_base_url}/${employee.uuid}`;

        employeeTableBody.append(
            `<tr>
                <td class="text-center">${i + 1}</td>
                <td>${employee.name}</td>
                <td class="text-center">${employee.date_of_birth}</td>
                <td class="text-center">${employee.salary}</td>
                <td>${employee.department.name} (${employee.department.organisation})</td>
                <td>
                    <a href="${edit_employee_url}" style="text-decoration:none;">
                        <span class="glyphicon glyphicon-pencil"></span>
                        <span>Edit</span>
                    </a>
                </td>
                <td>
                    <a class = "delete" href="${delete_employee_url}">
                        <span class="glyphicon glyphicon-trash"></span>
                        <span>Delete</span>
                    </a>
                </td>
            </tr>`
        );
    }
}
