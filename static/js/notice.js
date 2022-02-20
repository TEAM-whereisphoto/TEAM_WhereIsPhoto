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
            circleDiv.setAttribute('id', "notice__badge")
            circleDiv.setAttribute('class', "position-absolute top-0 translate-middle-y badge rounded-pill bg-danger")
            if (notice_num >= 10) {
                circleDiv.innerHTML = "10+"
                circleDiv.setAttribute('style', 'font-family: SUIT-medium; font-size: .5rem; left: 75% !important; padding: .35em .5em !important;');
            }
            else {
                circleDiv.innerHTML = notice_num
                circleDiv.setAttribute('style', 'font-family: SUIT-medium; font-size: .5rem; left: 75% !important;');
            }
            mypageBtn.children[0].append(circleDiv)
        }
    })
})