getData('/api/v1/ticket/me', sessionStorage.getItem('token'))
    .then((data) => {
        for (const [index, item] of data.entries()) {
            document.getElementById('tableMyTickets').innerHTML += `<tr onclick="window.location='/ticket/${item['id']}'"> <th scope="row">${index}</th> <td>${item['header']}</td> <td>${item['text']}</td></tr>`
        }
    })

    getData('/api/v1/ticket/assingt', sessionStorage.getItem('token'))
    .then((data) => {
        for (const [index, item] of data.entries()) {
            document.getElementById('tableAssingtTickets').innerHTML += `<tr onclick="window.location='/ticket/${item['id']}'"> <th scope="row">${index}</th> <td>${item['header']}</td> <td>${item['text']}</td></tr>`
        }
    })