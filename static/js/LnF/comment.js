const requestComment = new XMLHttpRequest();
const requestDel = new XMLHttpRequest();
const requestTag = new XMLHttpRequest();

const checkboxes = document.querySelectorAll("input[type=checkbox][name=tag]")
const checkDict = {'분실': true, '보관': true}

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

checkboxes.forEach(function(checkbox){
    checkbox.addEventListener("change", function(){
        const url = "tag/"
        const value = checkbox.value;
        const checkedIdx = (checkbox.checked == true)
        const query = document.getElementById('query').value
        checkDict[value] = checkedIdx
        requestTag.open("POST", url, true);
        requestTag.setRequestHeader(
            "Content-Type", "application/x-www-form-urlencoded"
        );
        requestTag.send(JSON.stringify({'분실': checkDict['분실'], '보관': checkDict['보관'], 'query': query }))
        })
    
})

//from server
const addComment = () => {
    if (requestComment.status < 400){
        const {id, type, content, comment_id} = JSON.parse(requestComment.response)
        //댓글 추가하기
        // element(table, #comment-table-{post.id}) 
        //  -> new_comment(tr, #comment-{comment.id})  
        //      -> comment_content(td)
        //      -> del-btn(button)
        
        const element = document.querySelector(`#comment-table-${id}`)
        const new_comment = document.createElement("tr")
        const comment_content = document.createElement("td")        
        const del_btn = document.createElement("button")
        
        //comment 내용 채우기
        comment_content.append(content)
        //tr attribute
        comment_content.setAttribute("id", `comment-${comment_id}`)
        //button attribute
        del_btn.setAttribute("class", "del_btn")
        del_btn.setAttribute("onclick","onClickComment({{comment.id}}, 'del')")
        del_btn.innerHTML = "삭제"
        //input 칸 리셋
        document.getElementById(`comment_input-${id}`).value = ''
        
        //skeleton
        element.append(new_comment)
        new_comment.appendChild(comment_content)
        new_comment.appendChild(del_btn)
    }
}

const delComment = () => {
    if (requestComment.status < 400){
        const{id} = JSON.parse(requestDel.response)
        
        const element = document.querySelector(`#comment-${id}`)
        element.remove();
        
    }
}

const filterByTag = () =>{
    if (requestTag.status < 400){
        const {resList, query} = JSON.parse(requestTag.response)

        const postList = document.querySelectorAll('#postList > div');
        for (const div of postList){
            div.remove();
        }
        const postListSection = document.querySelector('#postList');
        
        for (const post of resList){
            const container = document.createElement('div')

            container.innerHTML=`<div>
            <a href="{% url 'LnF:detail' ${post.booth_id} %}">부스명: ${post.booth_name}</a>
            <div>
                태그: ${post.tag}
            </div>
            <div>
                내용: ${post.content}
            </div>
            <div>
                작성자: ${post.user}<br>
            </div>`
            
            const timeDiv = document.createElement('div')
            const imgDiv = document.createElement('div')

            const timeString = post.timeString
            if (timeString == false){
                timeDiv.innerHTML = '작성시간: '+ post.time
            }
            else{
                timeDiv.innerHTML = '작성시간: ' + post.timeString
            }

            if (post.img != ''){
                const img = document.createElement('img')
                img.setAttribute("src", post.img)
                img.setAttribute("width", 300)
                imgDiv.append(img)
            }


            container.append(timeDiv)
            container.append(imgDiv)

            postListSection.append(container)
        }
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

requestTag.onreadystatechange = () => {
    if(requestTag.readyState === XMLHttpRequest.DONE){
        filterByTag();
    
    }
}