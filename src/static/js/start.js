
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
if ((sessionStorage.getItem('token') === "null") || sessionStorage.getItem('token') === "undefined" ) {
    document.location.href = "/login"
} else {
    console.log(sessionStorage.getItem('token'))
    getData('/api/v1/ticket/me', sessionStorage.getItem('token'))
        .then((data) => {
            console.log(data);
            for (const [index, item] of data.entries()) {
                document.getElementById('tableMyTickets').innerHTML += `<tr onclick="window.location='/ticket/${item['id']}'"> <td>${item['header']}</td> <td style="color: ${item['color']}">${item['p.text']}</td>  <td>${item['c.text']}</td> </tr>`
            }
        })
    getData('/api/v1/ticket/assingt', sessionStorage.getItem('token'))
        .then((data) => {
            console.log(data);
            for (const [index, item] of data.entries()) {
                document.getElementById('tableAssingtTickets').innerHTML += `<tr onclick="window.location='/ticket/${item['id']}'"> <td>${item['header']}</td> <td style="color: ${item['color']}">${item['p.text']}</td>  <td>${item['c.text']}</td> </tr>`
            }
        })
}
function logout() {
    sessionStorage.setItem('token', null)
    document.location.href = "/login";
}