const requestComment = new XMLHttpRequest();
const requestDel = new XMLHttpRequest();

// to server
const onClickComment = (id, type) => {
    const url = "add_comment/";
    const content = document.getElementById(`comment_input-${id}`).value
    requestComment.open("POST", url, true);
    requestComment.setRequestHeader(
        "Content-Type", "application/x-www-form-urlencoded"
    );
    requestComment.send(JSON.stringify({id: id, type: type, "content": content}))
}

const onClickDel = (id) => {
    const url = "del_comment/";
    requestDel.open("POST", url, true);
    requestDel.setRequestHeader(
        "Content-Type", "application/x-www-form-urlencoded"
        );
        requestDel.send(JSON.stringify({id: id}))
    }

//from server
const addComment = () => {
    if (requestComment.status < 400){
        const {id, type, content, comment_id, user, time} = JSON.parse(requestComment.response)
        //댓글 추가하기
        // element(table, #comment-table-{post.id}) 
        //  -> new_comment(tr, #comment-{comment.id})  
        //      -> comment_content(td)
        //      -> del-btn(button)
        
        const element = document.querySelector(`#comment-table-${id}`)
        const new_comment = document.createElement("tr")
        
        new_comment.innerHTML = `<tr id = "comment-${comment_id}">
        <td>댓글내용: ${content}</td>
        <td>댓글 작성자: ${user}</td>
        <td>
            작성시간: 방금 전
            </td>
            <td>
            <button class="del-btn" onclick="onClickDel(${comment_id})">삭제</button>
            </td>
            </tr>`
            
            //input 칸 리셋
        document.getElementById(`comment_input-${id}`).value = ''

            
        element.append(new_comment)
            
        }
}

const delComment = () => {
    if (requestComment.status < 400){
        const{id} = JSON.parse(requestDel.response)
        
        const element = document.querySelector(`#comment-${id}`)
        element.remove();
        
    }
}

// request
requestComment.onreadystatechange = () => {
    if(requestComment.readyState === XMLHttpRequest.DONE){
        addComment();
    }
}
requestDel.onreadystatechange = () => {
    if(requestDel.readyState === XMLHttpRequest.DONE){
        delComment();
    }
}
