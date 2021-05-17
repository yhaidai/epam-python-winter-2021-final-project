$(document).ready(function () {
    fetch('/api/departments')
        .then((response) => response.json())
        .then((departments) => {
            initDepartmentSelect(departments);
        })
        .catch((err) => {
            console.log(err);
        });
});

function initDepartmentSelect(departments) {
    // initialize options
    departments.forEach(department => {
        $("#select-department").append(
            `<option value="${department.uuid}">
                ${department.name} (${department.organisation})
            </option>`
        )
    });

    // initialize table with first department's employees
    initEmployeesTable(departments[0].employees);

    // reinitialize table on option change
    $("#select-department").change(function () {
        let departmentUUID = $("#select-department option:selected").val();
        let department = departments.filter(function (department) {
            return department.uuid === departmentUUID;
        })[0];
        initEmployeesTable(department.employees);
    });
}

function initEmployeesTable(employees) {
    let edit_employee_base_url = $("#edit-employee-url").data().url
    let delete_employee_base_url = $("#delete-employee-url").data().url
    let table = $("#employees-table tbody")

    table.empty()
    for (let i = 0; i < employees.length; i++) {
        let employee = employees[i]
        let edit_employee_url = `${edit_employee_base_url}/${employee.uuid}`
        let delete_employee_url = `${delete_employee_base_url}/${employee.uuid}`

        table.append(
            `<tr>
                <td class="text-center">${i + 1}</td>
                <td>${employee.name}</td>
                <td class="text-center">${employee.date_of_birth}</td>
                <td class="text-center">${employee.salary}</td>
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
