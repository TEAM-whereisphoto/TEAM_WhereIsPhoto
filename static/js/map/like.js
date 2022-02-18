const onClickLike = (booth_id) => {
    fetch(`${booth_id}/like_ajax/`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        booth_id = data['booth_id'];
        const heart = document.getElementById("heart_container")
        heart.innerHTML = `<div class="detail__heart" onclick="onClickDislike(${booth_id})">♥ 여기 매장 좋아요!</div>`
    })
}

const onClickDislike = (booth_id) => {
    fetch(`${booth_id}/dislike_ajax/`)
    .then(response => {
        return response.json()
    })
    .then(data => {
        booth_id = data['booth_id'];
        const heart = document.getElementById("heart_container")
        heart.innerHTML = `<div class="detail__noheart" onclick="onClickLike(${booth_id})" >♥ 여기 매장 좋아요!</div>`
    })
}

const onClickAlert = () =>{
    alert('로그인을 먼저 해주세요.!')
    window.location.href ='/user/login'
}

// ------------------------------------------------------------
// tag fill 채우기
document.addEventListener("DOMContentLoaded", function(event){
    // your code here
    const tagfills = this.getElementsByClassName("tag__fill")
    for (let eachtag of tagfills) {
        let width = eachtag.dataset.num / eachtag.dataset.reviews * 100
        console.log(width)
        eachtag.setAttribute("style", `width: ${width}%`)
    }
    
});
