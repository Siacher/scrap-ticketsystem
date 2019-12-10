getData('/api/v1/category/me', sessionStorage.getItem('token'))
.then((data) => {
    for (const [index, item] of data.entries()) {
        document.getElementById('tableMyCategories').innerHTML += `<tr onclick="window.location='/category/${item['id']}'"> <th scope="row">${index}</th> <td>${item['header']}</td> <td>${item['text']}</td></tr>`
    }
})

getData('/api/v1/category/assingt', sessionStorage.getItem('token'))
.then((data) => {
    for (const [index, item] of data.entries()) {
        document.getElementById('tableAssingtCategories').innerHTML += `<tr onclick="window.location='/category/${item['id']}'"> <th scope="row">${index}</th> <td>${item['header']}</td> <td>${item['text']}</td></tr>`
    }
})
