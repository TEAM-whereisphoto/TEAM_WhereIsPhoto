const requestTag = new XMLHttpRequest();

const checkboxes = document.querySelectorAll("input[type=checkbox][name=tag]")
const checkDict = {'분실': true, '보관': true}
console.log(checkboxes)
checkboxes.forEach(function(checkbox){
    checkbox.addEventListener("change", function(){
        const url = "tag/"
        var value = checkbox.value;
        var checkedIdx = (checkbox.checked == true)
        checkDict[value] = checkedIdx
        
        const query = document.getElementById('query').value
        requestTag.open("POST", url, true);
        requestTag.setRequestHeader(
            "Content-Type", "application/x-www-form-urlencoded"
        );
        requestTag.send(JSON.stringify({'분실': checkDict['분실'], '보관': checkDict['보관'], 'query': query }))
    })
    
})
const filterByTag = () =>{
    if (requestTag.status < 400){
        const {resList} = JSON.parse(requestTag.response)
        // console.log(resList)
        const postList = document.querySelectorAll('#postList > div > div');
        for (const div of postList){
            div.remove();
        }
        // 목록 다 삭제

        const postListSection = document.querySelector('#postList');
        
        for (const post of resList){
            const container = document.createElement('div')

            const timeString = post.timeString
            if (timeString == false){
                var timetext = post.time
            }
            else{
                var timetext = post.timeString
            }

            if (post.img == "") {
                var imgif = post.img
            }
            else { var imgif = '<img src="' + post.img + '" alt="" width="100%"></img>' }

            container.innerHTML=`
            <div class="post shadow p-3">
                <div class="post__title">
                    <span class="post__${ post.tag }">${post.tag}</span>
                    <a href="/LnF/${post.id}/post_detail/">${post.booth_name}</a>
                </div>
                <div style="height: .5rem;"></div>
                <div class="post_content">
                    ${post.content} <br>
                    ${imgif}
                </div>
                <div style="height: .5rem;"></div>
                <div class="post__footer">
                    <div>
                        ${post.user}<br>
                    </div>
                    <div>
                        ${timetext}
                    </div>
                </div>          
            </div>`
            
            postListSection.children[0].append(container)
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