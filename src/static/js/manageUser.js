getData('/api/v1/user/group', sessionStorage.getItem('token'))
    .then((data) => {
        console.log(data);

        if (data["message"] == "not authorized") {

        } else {
            for (var item of data['message']) {
                document.getElementById('tableUserRoles').innerHTML += `<tr> <td>${item['first_name']} ${item['last_name']}</td> <td>${item['email']}</td> <td class="role_name" id="${item['group_id']}_${item['user_id']}">${item['name']}</td></tr>`

            }
        }
    })

function editMode() {
    role_cols = document.getElementsByClassName('role_name')
    getData('/api/v1/user_group', sessionStorage.getItem('token'))
        .then((data) => {
            console.log(data);

            document.getElementById('buttonMenue').innerHTML = '<button class="btn btn-sm btn-outline-success" onclick="save()">save</button>\n<button class="btn btn-sm btn-outline-danger" onclick="cancel()">cancel</button>'

            for (var node of role_cols) {
                var node_id = node['id'].split("_")[0]
                var options = ""
                for (var item of data['data']) {
                    if (item['id'] == node_id) {
                        options += `<option selected id=${item.id}> ${item.name} </option>\n`

                    } else {
                        options += `<option id=${item.id}> ${item.name} </option>\n`
                    }

                }
                node.innerHTML = `<select id="inputGroup${node.id}" class="form-control"> ${options}</select>`
            }
        })
}

function save() {
    var role_cols = document.getElementsByClassName('role_name')

    var loop = async _ => {
        for (var node of role_cols) {
            var role_id = node['id'].split("_")[0]
            var user_id = node['id'].split("_")[1]

            var e = node.firstChild;
            var sel_role = e.options[e.selectedIndex];

            if (!(role_id == sel_role.id)) {
                var new_role_id = sel_role.id;
                var data = { "group_id": role_id, "user_id": user_id, "new_group_id": new_role_id }

                console.log(data)

                await postData("/api/v1/user/change_group", data, sessionStorage.getItem('token'))

            }
        }
    }
    loop().then(() => {
        document.location.reload();
    })

}

function cancel() {
    document.location.reload();
}
