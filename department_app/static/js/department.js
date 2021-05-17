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
    $("#add-department-form").submit(function(event) {
        let data = {
            name: $("#add-name").val(),
            organisation: $("#add-organisation").val()
        }

        fetch("/api/departments/", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(checkStatus)
            .then((response) => response.json())
            .then((department) => {
                alert(`Successfully added department: 
                ${JSON.stringify(department)}`);
            })
            .catch((err) => {
                console.log(err);
                alert("Failed to add department", false);
            });
    });
}

function initEditDepartmentForm(departments) {
    initDepartmentSelect("#edit-select-department", departments);
    initDepartmentInputs("#edit-select-department", "#edit-name", "#edit-organisation");

    $("#edit-select-department").change(function() {
        initDepartmentInputs("#edit-select-department", "#edit-name", "#edit-organisation");
    });

    $("#edit-department-form").submit(function(event) {
        let uuid = $("#edit-select-department option:selected").val();
        let data = {
            name: $("#edit-name").val(),
            organisation: $("#edit-organisation").val(),
        }

        fetch(`/api/department/${uuid}`, {
            method: "PUT",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(checkStatus)
            .then((response) => response.json())
            .then((department) => {
                alert(`Successfully edited department: 
                ${JSON.stringify(department)}`);
            })
            .catch((err) => {
                console.log(err);
                alert("Failed to edit department", false);
            });
    });
}

function initDeleteDepartmentForm(departments) {
    initDepartmentSelect("#delete-select-department", departments);

    $("#delete-department-form").submit(function(event) {
        let uuid = $("#delete-select-department option:selected").val();

        fetch(`/api/department/${uuid}`, {
            method: "DELETE",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
        })
            .then(checkStatus)
            .then((response) => {
                alert("Successfully deleted");
            })
            .catch((err) => {
                console.log(err);
                alert("Failed to deleted department", false);
            });
    });
}

function initDepartmentSelect(selectId, departments) {
    // initialize options
    departments.forEach(department => {
        $(selectId).append(
            `<option value="${department.uuid}">
                ${department.name} (${department.organisation})
            </option>`
        )
    });
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

function checkStatus(response) {
    if (response.ok) {
        return Promise.resolve(response);
    } else {
        return Promise.reject(new Error(response.statusText));
    }
}

function alert(message, success = true) {
    let cls = 'alert alert-success alert-dismissible fade in text-center'
    if (!success) {
        cls = 'alert alert-danger alert-dismissible fade in text-center'
    }

    $("body").prepend(
        `<div id="alert" class="${cls}">
            <a href="#" class="close" data-dismiss="alert" 
            aria-label="close">&times;</a>
            <strong>${message}</strong>
        </div>`
    )
    setTimeout(() => {
        $("#alert").remove()
    }, 10000);
}
