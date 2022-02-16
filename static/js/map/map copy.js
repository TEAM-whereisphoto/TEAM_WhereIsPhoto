// 지도 자체 초기 설정
var container = document.getElementById('map');
var options = {
    center: new kakao.maps.LatLng(37.557074, 126.929276), // 임의의 중심 좌표
    level: 4 // 확대 축소 정도
};

var map = new kakao.maps.Map(container, options); // 지도 생성
var bounds = map.getBounds(); // 지도 범위 가져오는 bounds 변수 초기값 생성

// 지도에 표시된 마커 객체를 가지고 있을 배열입니다
var markers = [];

// 표시할 매장 이름. 나중에 brand model에서 가져오도록 수정 예정.
var filterSet = new Set(['인생네컷', '포토이즘박스', '포토시그니처', '셀픽스', '하루필름']);

// 지도 확대 축소 컨트롤 생성
var zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.LEFT);


// blue pin으로 된 marker image 생성
// 브랜드별 색깔 바꿀 때 이 부분 src 수정, 혹은 실제 pin 박을 때 수정도 가능
// 참고 -> 이 api에서는 href 링크나 실제 이미지로만 pin 이미지 설정 가능. <i> rexicon꺼 </i> 등 형태 불가. 
var imageSrc = '../static/icons/pin_blue.png'
var imageSize = new kakao.maps.Size(28, 28);
var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 

const lifepin = new kakao.maps.MarkerImage('../static/icons/lifefourcuts.svg', imageSize)
const selfixpin = new kakao.maps.MarkerImage('../static/icons/selfix.svg', imageSize)
const photoismpin = new kakao.maps.MarkerImage('../static/icons/photoism.svg', imageSize)
const harupin = new kakao.maps.MarkerImage('../static/icons/harufilm.svg', imageSize)
const signaturepin = new kakao.maps.MarkerImage('../static/icons/signature.svg', imageSize)
var brandpin = null;

// 1 현재 위치 찍기 -----------------------------------------------------------------------------

// 현재 위치 차단 확인하는 코드  https://kjwan4435.tistory.com/66
var gps_use = null; //gps의 사용가능 여부
var gps_lat = null; // 위도
var gps_lng = null; // 경도
var gps_position; // gps 위치 객체

gps_check();
// gps가 이용가능한지 체크하는 함수이며, 이용가능하다면 show location 함수를 불러온다.
// 만약 작동되지 않는다면 경고창을 띄우고, 에러가 있다면 errorHandler 함수를 불러온다.
// timeout을 통해 시간제한을 둔다.
function gps_check(){

    if (navigator.geolocation) {
        var options = {timeout:60000};
        navigator.geolocation.getCurrentPosition(showLocation, errorHandler, options);
    } else {
        alert("GPS_추적이 불가합니다.");
        gps_use = false;
    }
}

// gps 이용 가능 시, 위도와 경도를 반환하는 showlocation함수.
function showLocation(position) {
    gps_use = true;
    gps_lat = position.coords.latitude;
    gps_lng = position.coords.longitude;

    var currentPosition  = new kakao.maps.LatLng(gps_lat,gps_lng); // 현재 위치정보로 위치객체 생성
            
    var marker = new kakao.maps.Marker({  
        map: map, 
        position: currentPosition, 
        image: new kakao.maps.MarkerImage('../static/icons/pin_current.png', new kakao.maps.Size(24, 24))
        // 현재 위치는 빨간색 pin_current로 이미지 설정해둠
    }); 

    marker.setMap(map); // 내 위치 pin 박기
    map.setCenter(currentPosition); // 내 위치를 중심 좌표로 이동
    map.setLevel(7);
    bounds = map.getBounds(); // 새로 bound 가져오기.
}


// error발생 시 에러의 종류를 알려주는 함수.
function errorHandler(error) {
    if(error.code == 1) {
        alert("위치 엑세스가 거부되었습니다.\n기본 위치로 이동합니다.");
    } else if( err.code == 2) {
        alert("위치를 반환할 수 없습니다.");
    }
    gps_use = false;
    // 이 경우 bound는 처음에 설정한 값으로 유지됨 (변경 x)
}



// 2 부스 표시하기 -----------------------------

// 주소 정보 가져오기
// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

// 일단 render로 넘어온 모든 booth들 안보이게 boothList에 등록
// 이 부분은 추후 상의해봐야할듯 함.. 다 갖고오고 for문 돌려서 새로 표시만 하니까 로딩 너무 느려 ㅠ
var boothList = document.getElementById('boothList');
let total = boothList.childElementCount; // count booths    

// booth list하는 아코디언 dom
var accList = document.getElementById('accordionList')
// 범위 내의 booth list 저장해두는 array
let mapboundbooth = []

function for_pin(total){
    for (let i=0; i<total; i++) {
        setbooth(i);
        // pin은 다 찍고, list는 현재 중심좌표(내 위치든 기본값이든) 주변으로만 표시
    }
}

for_pin(total);

function setbooth(i) {
    let booth = boothList.children[i] // 특정 booth 정보 담은 객체
    // let booth = boothparent.firstElementChild.dataset
    const name = booth.firstElementChild.dataset.name
    const brandname = booth.firstElementChild.dataset.brand
    // console.log(brandname)
    const mapLat = booth.firstElementChild.dataset.x
    const mapLng = booth.firstElementChild.dataset.y


    // 특정 pin's infowindow 설정
    var content = '<div style="padding:2px;z-index:1;font-size:8px; text-align: center!important;">' + name + '</div>';
    var infowindow = new kakao.maps.InfoWindow({zIndex:1}); // 새 info object
    infowindow.setContent(content); // infowindow 내용

    
    switch (brandname) {
        case '하루필름':
            console.log("하루")
            brandpin = harupin;
            break;
        case '인생네컷':
            console.log("인생")
            brandpin = lifepin;
            break;
        case '포토이즘박스':
            console.log("포토")
            brandpin = photoismpin;
            break;
        case '셀픽스':
            console.log("셀")
            brandpin = selfixpin;
            break;
        case '포토시그니처':
            console.log("시그")
            brandpin = signaturepin;
            break;
        default:
            brandpin = markerImage;
            console.log("이거 표시되면 안된다 뭔가 잘못되고 있는거다?")
    }

    var coords = new kakao.maps.LatLng(mapLat, mapLng) 
    addMarker(coords, brandpin, infowindow);
    // 초기 607개 pin 배열 생성

    infowindow.setPosition(coords); // 인포윈도우 달릴 위치 설정 (=해당 핀 좌표)


    
    // booth의 좌표가 현재 지도 boundary 안에 있는거면 list
    if (bounds.contain( coords )) {
        printList(booth); // list에 표시하기             
        mapboundbooth.push(booth);           
        console.log("위치 안")
    }

}

function addMarker(pos, img, infowindow) {
    var marker = new kakao.maps.Marker({
        map:map,
        position: pos,
        image: img,
    });
    marker.setMap(map);
    markers.push(marker);
    
    setClickEvents(marker, infowindow);


}

function setClickEvents (marker, infowindow) { // 파라미터
    // 마커에 mouseover 이벤트를 등록하고 마우스 오버 시 인포윈도우를 표시합니다 
    kakao.maps.event.addListener(marker, 'mouseover', function() {
        infowindow.open(map, marker);
    });

    // 마커에 mouseout 이벤트를 등록하고 마우스 아웃 시 인포윈도우를 닫습니다
    kakao.maps.event.addListener(marker, 'mouseout', function() {
        infowindow.close();
    });

    // 이 아래는 list에 mouseover시 하려고 했던 것
    // 추후 디자인 logic 따라 수정 예정

    // name_ele.onmouseover =  function () {
    //     infowindow.open(map, marker);
    // };

    // name_ele.onmouseout =  function () {
    //     infowindow.close();
    // };
    // console.log("set hover func");
};

// 3 초기 세팅 이후, 화면 변경에 따라 list 표시 다르게
// 중심 좌표 움직였을 때
kakao.maps.event.addListener(map, 'center_changed', findList);
// 확대 축소 했을 때
kakao.maps.event.addListener(map, 'zoom_changed', findList)


function findList() {
    accList.innerHTML = '';
    // 이미 되어있던 acc 리스트 초기화
    mapboundbooth = []

    bounds = map.getBounds(); // 화면 변경되었으니 범위 다시 가져오고

    for (let i=0; i<total; i++) {
    
        let booth = boothList.children[i]
        let lat = booth.firstElementChild.dataset.x
        let lng = booth.firstElementChild.dataset.y
        boothcoord = new kakao.maps.LatLng(lat, lng)
        
        // booth의 좌표가 현재 지도 boundary 안에 있는거면 list
        if (bounds.contain( boothcoord )) {

            printList(booth); // list에 표시하기
            mapboundbooth.push(booth)           
        }
    
        else {
            // console.log("not in map")
        }  
    }

}

// 리스트에 매장 추가
// 근데 넘 느려ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ
function printList(boothElement) {
    
    const brand = boothElement.firstElementChild.dataset.brand;

    // if (!filterSet.has(brand)) {
    //     return 0;
    // }

    // 지도 내에 있는 booth의 정보 가져오기
    let name = boothElement.firstElementChild.dataset.name; // ???????????
    let address = boothElement.firstElementChild.dataset.loc;
    const boothId = boothElement.firstElementChild.dataset.id;
    const hour = boothElement.firstElementChild.dataset.hour;
    

    const street = parseInt(boothElement.firstElementChild.dataset.street);
    const deco = parseInt(boothElement.firstElementChild.dataset.deco);
    const boxnum = parseInt(boothElement.firstElementChild.dataset.boxnum);
    const rating = parseFloat(boothElement.firstElementChild.dataset.rating);
    const likenum = boothElement.firstElementChild.dataset.likenum;
    
    let streetContent = ''
    let decoContent = ''
    let hourContent = ''

    // detail 어떻게 표시될지 if문
    if (street) { streetContent = "매장점" }
    else { streetContent = "부스점" }

    if (deco) { decoContent = "○" } // 소품 ㅇ
    else { decoContent = "X" } // 소품 x

    if (hour) { hourContent = hour } // 시간 null 아닌 경우만 표시

    const newdiv = document.createElement('div');
    newdiv.setAttribute('class', 'accordion-item');
    newdiv.innerHTML = 
    `<div class="accordion-item">
        <h2 class="accordion-header">
            <button id="accordion-name" data-name="${ name }" class="accordion-button collapsed fs-5" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${ boothId }" aria-expanded="true" aria-controls="collapse-${ boothId }">
                <svg class="me-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
                    <path fill="none" d="M0 0h24v24H0z"/>
                    <path d="M18.364 17.364L12 23.728l-6.364-6.364a9 9 0 1 1 12.728 0zM12 13a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" fill="rgba(31,82,255,1)"/>
                </svg>${ name }

                <button class="btn btn-gray btn-sm ms-5 mb-3">${ brand }</button>
            </button>
        </h2>

        <div id="collapse-${ boothId }" class="accordion-collapse collapse" aria-labelledby="heading-${ boothId }" data-bs-parent="#accordionList">
            <div class="accordion-body">
                <div id="mapdetail-${ boothId }" class="ps-4">
                    
                    <p style="margin: 0; color: #8B8B8B; font-size: 0.75rem;">
                        부스 ${ boxnum }개 | ${ streetContent } | 소품 ${ decoContent }
                    </p>
                    
                    <p style="margin: 16px 0 0 0">${ address }</p>

                    <p style="margin: 16px 0 0 0"></p>
                    ${ hourContent }
                    </p>

                    <button class="btn btn-outline-ratingNlike container" style="width: 75%;">
                        <div class="row">

                            <div class = "col" style="color: #FFD107;">★ ${ rating }</div>
                            | 
                            <div class = "col" style="color: #484848"> ${ likenum } users </div>
                        </div>
                    </button>

                    <a style="display: block;" class="mt-3" href="/booth/detail/${ boothId }">디테일페이지</a>
                </div>
            </div>
        </div>
    </div>`;

    accList.append(newdiv); // list추가
}

// 4. 정렬 필터
// alphabet
var sortAlpha = document.getElementById('sortAlpha');
var sortAlphaDesc = document.getElementById('sortAlphaDesc');
var sortDist = document.getElementById('sortDist'); // 구현 전

sortAlpha.addEventListener('click', function() {
    
    if (this.checked) {
        console.log("checked!")


        mapboundbooth.sort(function(a, b) {
            var nameA = a.firstElementChild.dataset.name; // ignore upper and lowercase
            var nameB = b.firstElementChild.dataset.name; // ignore upper and lowercase
            if (nameA < nameB) {
            return -1;
            }
            if (nameA > nameB) {
            return 1;
            }
        
            // 이름이 같을 경우
            return 0;
        });
        accList.innerHTML = '';

        for (var index in mapboundbooth) {
            printList(mapboundbooth[index], accList);
        }
    }
});

sortAlphaDesc.addEventListener('click', function() {
    
    if (this.checked) {
        console.log("desc checked!")
    

        mapboundbooth.sort(function(a, b) {
            var nameA = a.firstElementChild.dataset.name; // ignore upper and lowercase
            var nameB = b.firstElementChild.dataset.name; // ignore upper and lowercase
            if (nameA > nameB) {
            return -1;
            }
            if (nameA < nameB) {
            return 1;
            }
        
            // 이름이 같을 경우
            return 0;
        });
        accList.innerHTML = '';

        for (var index in mapboundbooth) {
            printList(mapboundbooth[index], accList);
        }
    }
});

// 거리순 정렬 아직 미구현. default로 할까 생각중.


// 5. 브랜드 필터
const filterLifefour = document.getElementById('filter-lifefour');
const filterPhotoism = document.getElementById('filter-photoism');
const filterSignature = document.getElementById('filter-signature');
const filterSelfix = document.getElementById('filter-selfix');
const filterHaru = document.getElementById('filter-haru');

const filterGroup = document.getElementById('filterGroup');

const requestFilter = new XMLHttpRequest();

filterGroup.addEventListener('click', function() {

    hideMarkers();

    for (let i=1; i<this.childElementCount; i=i+2) {
        brandname = this.children[i].innerHTML;
        if (this.children[i-1].checked) { filterSet.add(brandname) }
        else { filterSet.delete(brandname) }
    }

    const url = "/filter/";
    requestFilter.open("POST", url, true);
    requestFilter.setRequestHeader(
        "Content-Type",
        "application/x-www-form-urlencoded"
    );
    // set 자료구조는 json안에 못들어가나?
    console.log("before sending to view");
    console.log(filterSet);
    let array = Array.from(filterSet);
    // const jsoned = JSON.stringify({brands: String(array)});
    const jsoned = JSON.stringify({brands: array});
    console.log(jsoned)
    requestFilter.send(jsoned);



    // for (let i=1; i<this.childElementCount; i=i+2) {
    //     brandname = this.children[i].innerHTML;
    //     if (this.children[i-1].checked) { filterSet.add(brandname) }
    //     else { filterSet.delete(brandname) }
    // }

    // console.log(filterSet)
    // accList.innerHTML = '';

    // for (var index in mapboundbooth) {
    //     printList(mapboundbooth[index], accList);
    // }
    
});

const filterHandleResponse = () => {
    if(requestFilter.status < 400 ) { // 응답이 왔고, 거기에 오류가 있나 (서버 에러, 다른 에러 505 등)
        const filteredbooths = JSON.parse(requestFilter.response);
        
        accList.innerHTML = '';
        console.log(filteredbooths)

        for (let booth of filteredbooths) {
        // refreshpin(filteredbooths);
            // addMarker()

        // listup(filteredbooths);
        // 구현해야함. 일단 밑에 적어두겠음

            const brand = booth.brand;

            // 지도 내에 있는 booth의 정보 가져오기
            let name = booth.name; // ???????????
            let address = booth.loc;
            const boothId = booth.id;
            const hour = booth.hour;
            

            const street = parseInt(booth.street);
            const deco = parseInt(booth.deco);
            const boxnum = parseInt(booth.boxnum);
            const rating = parseFloat(booth.rating);
            const likenum = booth.likenum;

            let streetContent = ''
            let decoContent = ''
            let hourContent = ''

            // detail 어떻게 표시될지 if문
            if (street) { streetContent = "매장점" }
            else { streetContent = "부스점" }

            if (deco) { decoContent = "○" } // 소품 ㅇ
            else { decoContent = "X" } // 소품 x

            if (hour) { hourContent = hour } // 시간 null 아닌 경우만 표시

            const newdiv = document.createElement('div');
            newdiv.setAttribute('class', 'accordion-item');
            newdiv.innerHTML = 
            `<div class="accordion-item">
                <h2 class="accordion-header">
                    <button id="accordion-name" data-name="${ name }" class="accordion-button collapsed fs-5" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${ boothId }" aria-expanded="true" aria-controls="collapse-${ boothId }">
                        <svg class="me-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
                            <path fill="none" d="M0 0h24v24H0z"/>
                            <path d="M18.364 17.364L12 23.728l-6.364-6.364a9 9 0 1 1 12.728 0zM12 13a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" fill="rgba(31,82,255,1)"/>
                        </svg>${ name }

                        <button class="btn btn-gray btn-sm ms-5 mb-3">${ brand }</button>
                    </button>
                </h2>

                <div id="collapse-${ boothId }" class="accordion-collapse collapse" aria-labelledby="heading-${ boothId }" data-bs-parent="#accordionList">
                    <div class="accordion-body">
                        <div id="mapdetail-${ boothId }" class="ps-4">
                            
                            <p style="margin: 0; color: #8B8B8B; font-size: 0.75rem;">
                                부스 ${ boxnum }개 | ${ streetContent } | 소품 ${ decoContent }
                            </p>
                            
                            <p style="margin: 16px 0 0 0">${ address }</p>

                            <p style="margin: 16px 0 0 0"></p>
                            ${ hourContent }
                            </p>

                            <button class="btn btn-outline-ratingNlike container" style="width: 75%;">
                                <div class="row">

                                    <div class = "col" style="color: #FFD107;">★ ${ rating }</div>
                                    | 
                                    <div class = "col" style="color: #484848"> ${ likenum } users </div>
                                </div>
                            </button>

                            <a style="display: block;" class="mt-3" href="/booth/detail/${ boothId }">디테일페이지</a>
                        </div>
                    </div>
                </div>
            </div>`;

            accList.append(newdiv); // list추가

            }
        }
};

requestFilter.onreadystatechange = () => {
    if(requestFilter.readyState === XMLHttpRequest.DONE) {
        filterHandleResponse();
    }
}

function setMarkers(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }            
}

function showMarkers() {
    setMarkers(map);    
}

function hideMarkers() {
    setMarkers(null);    
}