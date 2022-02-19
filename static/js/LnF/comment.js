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

        // <table id="comment-table-{{post.id}}">
        //     {% for comment in post.comment_set.all %}
        //     <tr id = "comment-{{comment.id}}">
        //         <td>댓글내용: {{comment.content}}</td>
        //         <td>댓글 작성자: {{comment.user}}</td>
        //         <td>
        //             {% if comment.timeString == False %}
        //             작성시간: {{comment.time|date:'m월 d일'}}
        //             {% else %}
        //             작성시간: {{comment.timeString}}
        //             {% endif %}
        //         </td>
        //         <td>
        //             {% if comment.user == request.user %}
        //             <button class="del-btn" onclick="onClickDel({{comment.id}})">❌</button>
        //             {% endif %}                    
        //         </td>
        //     </tr>
        //     {% endfor %}
        // </table>

        // <tr id = "comment-${comment_id}">
        // <td>댓글내용: ${content}</td>
        // <td>댓글 작성자: ${user}</td>
        // <td>
        //     작성시간: 방금 전
        //     </td>
        //     <td>
        //     <button class="del-btn" onclick="onClickDel(${comment_id})">❌</button>
        //     </td>
        //     </tr>
        
        const element = document.querySelector(`#comment-table-${id}`)
        const new_comment = document.createElement("div")
        
        new_comment.innerHTML = `
        <div id="comment-${comment_id}" class="comment">
            <div class="between">
                <p style="margin:0; font-size:1rem">${content}</p>
                <button class="del-btn" onclick="onClickDel(${comment_id})">❌</button>
            </div>
            <div class="post__footer">
                <div>
                    ${user}
                </div>
                <div> 방금 전
                </div>
            </div>
        </div>
        `
            
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
