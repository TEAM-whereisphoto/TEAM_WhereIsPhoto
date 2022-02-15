document.addEventListener('DOMContentLoaded', function(){
    url = 'http://127.0.0.1:8000/'
    fetch(url+'user/nav_notice/')
    .then(response => {
        return response.json()
    })
    .then(data => {
        const notice = data['notice']
        if (notice == true){
            const mypageBtn = document.querySelector("body > header > div > div.navbar > div > a:nth-child(4)")
            const circleDiv = document.createElement("div")
            circleDiv.setAttribute('style', 'width:10px; height: 10px; border-radius:50%; background-color:red; z-index:3;')
            mypageBtn.append(circleDiv)
        }
    })
})