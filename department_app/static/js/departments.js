$(document).ready(function () {
    fetch("/api/departments")
        .then((response) => response.json())
        .then((departments) => {
            initDepartmentsTable(departments);
        })
        .catch((err) => {
            console.log(err);
        });
});

function initDepartmentsTable(departments) {
    let edit_department_base_url = $("#edit-department-url").data().url
    let delete_department_base_url = $("#delete-department-url").data().url

    for (let i = 0; i < departments.length; i++) {
        let department = departments[i]
        let edit_department_url = `${edit_department_base_url}/${department.uuid}`
        let delete_department_url = `${delete_department_base_url}/${department.uuid}`

        $("#departments-table tbody").append(
            `<tr>
                <td class="text-center">${i + 1}</td>
                <td>${department.name}</td>
                <td>${department.organisation}</td>
                <td class="text-center">${department.average_salary}$</td>
                <td>
                    <a href="${edit_department_url}" style="text-decoration:none;">
                        <span class="glyphicon glyphicon-pencil"></span>
                        <span>Edit</span>
                    </a>
                </td>
                <td>
                    <a class = "delete" href="${delete_department_url}">
                        <span class="glyphicon glyphicon-trash"></span>
                        <span>Delete</span>
                    </a>
                </td>
            </tr>`
        );
    }
}
