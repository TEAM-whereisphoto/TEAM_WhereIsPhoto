document.addEventListener('DOMContentLoaded', function(){
    url = 'http://127.0.0.1:8000/'
    fetch(url+'user/nav_notice/')
    .then(response => {
        return response.json()
    })
    .then(data => {
        const notice = data['notice']
        const notice_num = data['notice_num']
        if (notice == true){
            const mypageBtn = document.querySelector("body > nav > div > div:nth-child(3) > button")
            const circleDiv = document.createElement("div")
            circleDiv.setAttribute('class', "position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger")
            circleDiv.innerHTML = notice_num
            mypageBtn.append(circleDiv)
        }
    })
})