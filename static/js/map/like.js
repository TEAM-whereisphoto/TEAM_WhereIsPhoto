const onClickLike = (booth_id) => {
    fetch(`${booth_id}/like_ajax/`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        booth_id = data['booth_id'];
        const heart = document.querySelector("body > div > div:nth-child(1) > div")
        heart.innerHTML = `<div class="heart" onclick="onClickDislike(${booth_id})">❤️ 여기 매장 좋아요</div>`
    })
}

const onClickDislike = (booth_id) => {
    fetch(`${booth_id}/dislike_ajax/`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        booth_id = data['booth_id'];
        const heart = document.querySelector("body > div > div:nth-child(1) > div")
        heart.innerHTML = `<div class="heart" onclick="onClickLike(${booth_id})">🤍 여기 매장 좋아요</div>`
    })
}

const onClickAlert = () =>{
    alert('로그인을 먼저 해주세요.!')
    window.location.href ='{% url "user:login" %}'
}