let EDIT_DEPARTMENT_SELECT_ID = "#edit-select-department";
let DELETE_DEPARTMENT_SELECT_ID = "#delete-select-department";

let ADD_NAME_ID = "#add-name";
let ADD_ORGANISATION_ID = "#add-organisation";
let EDIT_NAME_ID = "#edit-name";
let EDIT_ORGANISATION_ID = "#edit-organisation";

let ADD_DEPARTMENT_FORM_ID = "#add-department-form";
let EDIT_DEPARTMENT_FORM_ID = "#edit-department-form";
let DELETE_DEPARTMENT_FORM_ID = "#delete-department-form";


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
    initAddDepartmentForm();
    initEditDepartmentForm(departments);
    initDeleteDepartmentForm(departments);
}

function initAddDepartmentForm() {
    $(ADD_DEPARTMENT_FORM_ID).submit(function (event) {
        let data = {
            name: $(ADD_NAME_ID).val(),
            organisation: $(ADD_ORGANISATION_ID).val()
        }

        fetchWithAlert(
            `/api/departments/`,
            "POST",
            "Successfully added department",
            "Failed to add department",
            data
        )
    });
}

function initEditDepartmentForm(departments) {
    initDepartmentSelect(EDIT_DEPARTMENT_SELECT_ID, departments);
    initDepartmentInputs(EDIT_DEPARTMENT_SELECT_ID, EDIT_NAME_ID, EDIT_ORGANISATION_ID);

    // reinitialise inputs on option change
    $(EDIT_DEPARTMENT_SELECT_ID).change(function () {
        initDepartmentInputs(EDIT_DEPARTMENT_SELECT_ID, EDIT_NAME_ID, EDIT_ORGANISATION_ID);
    });

    $(EDIT_DEPARTMENT_FORM_ID).submit(function (event) {
        let uuid = $(`${EDIT_DEPARTMENT_SELECT_ID} option:selected`).val();
        let data = {
            name: $(EDIT_NAME_ID).val(),
            organisation: $(EDIT_ORGANISATION_ID).val(),
        }

        fetchWithAlert(
            `/api/department/${uuid}`,
            "PUT",
            "Successfully edited department",
            "Failed to edit department",
            data
        )
    });
}

function initDeleteDepartmentForm(departments) {
    initDepartmentSelect(DELETE_DEPARTMENT_SELECT_ID, departments);

    $(DELETE_DEPARTMENT_FORM_ID).submit(function (event) {
        let uuid = $(`${DELETE_DEPARTMENT_SELECT_ID} option:selected`).val();

        fetchWithAlert(
            `/api/department/${uuid}`,
            "DELETE",
            "Successfully deleted department",
            "Failed to delete department"
        )
    });
}

function initDepartmentSelect(selectId, departments) {
    let url = (" " + window.location).slice(1)
    let urlSuffix = url.replace(window.origin, "")
    let urlParts = urlSuffix.split("/").filter(Boolean)
    let expanded = urlParts[1]
    let selectElement = $(selectId)

    // initialize options
    departments.forEach(department => {
        selectElement.append(
            `<option value="${department.uuid}">
                ${department.name} (${department.organisation})
            </option>`
        )
    });

    // select initial option
    if (selectId.includes(expanded) && expanded !== "add") {
        let uuid = urlParts[2].split('?')[0]
        selectElement.val(uuid)
    }
}

function initDepartmentInputs(selectId, nameInputId, organisationInputId) {
    let selected = $(`${selectId} option:selected`).text();
    let departmentRegexp = /(.*?)(?= \((.*)\))/;
    let match = departmentRegexp.exec(selected);
    let name = match[0].trim();
    let organisation = match[2].trim();
    $(nameInputId).val(name);
    $(organisationInputId).val(organisation);
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
