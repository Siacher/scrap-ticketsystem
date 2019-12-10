$(document).ready(function() {
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
});