$(document).ready(function () {
    fetch('/api/employees')
        .then((response) => response.json())
        .then((employees) => {
            initEmployeesTable(employees);
        })
        .catch((err) => {
            console.log(err);
        });
});

function initEmployeesTable(employees) {
    let edit_employee_base_url = $("#edit-employee-url").data().url
    let delete_employee_base_url = $("#delete-employee-url").data().url

    for (let i = 0; i < employees.length; i++) {
        let employee = employees[i]
        let edit_employee_url = `${edit_employee_base_url}/${employee.uuid}`
        let delete_employee_url = `${delete_employee_base_url}/${employee.uuid}`

        $("#employees-table tbody").append(
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
