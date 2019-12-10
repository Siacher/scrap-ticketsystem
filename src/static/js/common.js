if (!sessionStorage.getItem('token')) {
    document.location.href = "/login"
}

async function getData(url = '', token) {
    const response = await fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'token': token
        },
    });
    return await response.json();
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function createDropdown(url, token, elm_id) {
    getData(url, token)
        .then((data) => {
            if (data['data'].length > 0) {
                for (var item of data['data']) {
                    var elm = document.createElement('option')
                    elm.innerHTML = `<span id="${item.id}" >${item.text}<span>`
                    document.getElementById(elm_id).appendChild(elm)
                }
                document.getElementById(elm_id).disabled = false;
            }
        })
}