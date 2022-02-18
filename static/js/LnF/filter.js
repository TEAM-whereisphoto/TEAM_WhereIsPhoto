const requestTag = new XMLHttpRequest();

const checkboxes = document.querySelectorAll("input[type=checkbox][name=tag]")
const checkDict = {'분실': true, '보관': true}

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
const filterByTag = () =>{
    if (requestTag.status < 400){
        const {resList, query} = JSON.parse(requestTag.response)

        const postList = document.querySelectorAll('#postList > div > div');
        for (const div of postList){
            div.remove();
        }
        const postListSection = document.querySelector('#postList');
        
        for (const post of resList){
            const container = document.createElement('div')
            container.setAttribute

            container.innerHTML=`
            <div class="post shadow p-3">
                <div class="post__title">
                    <span class="post__${ post.tag }">${post.tag}</span>
                    <a href="/LnF/${post.booth_id}/detail/">${post.booth.name}</a>
                </div>
                <div style="height: .5rem;"></div>
                <!-- post content -->
                <div class="post_content">
                    ${post.content} <br>
                    {% if post.img %}
                    <img src="${post.img.url}" alt="" width="300"> 
                {% endif %}
                </div>
                <div style="height: .5rem;"></div>
                <!-- post footer -->
                <div class="post__footer">
                    <div>
                        ${post.user.username}}<br>
                    </div>
                    <div>
                        {% if post.timeString == False %}
                        {{post.time|date:'m월 d일'}}
                        {% else %}
                        {{post.timeString}}
                        {% endif %}
                    </div>
                </div>          
            </div>

            <div>
            <a href="/LnF/${post.booth_id}/detail/">부스명: ${post.booth_name}</a>
            <div>
                태그: ${post.tag}
            </div>
            <div>
                내용: ${post.content}
            </div>
            <div>
                작성자: ${post.user}<br>
            </div>
            `
            
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
requestTag.onreadystatechange = () => {
    if(requestTag.readyState === XMLHttpRequest.DONE){
        filterByTag();
    
    }
}

function delInput() {
    document.getElementById("query").value ='';
}
