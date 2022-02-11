
// 1. 지도 자체 초기 설정 -----------------------------------------------------------------------------
var container = document.getElementById('map');
var options = {
    center: new kakao.maps.LatLng(37.557074, 126.929276), // 임의의 중심 좌표
    level: 4 // 확대 축소 정도
};

var map = new kakao.maps.Map(container, options); // 지도 생성

// 지도 확대 축소 컨트롤 생성
var zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.LEFT);
// 지도 자체 초기 설정 끝 -----------------------------------------------------------------------------



// 2. 전역 변수들 생성 -----------------------------------------------------------------------------

// 표시할 brand 이름. 나중에 brand model에서 가져오도록 수정해두면 더 좋긴 할듯.
const filterSet = new Set(['인생네컷', '포토이즘박스', '포토시그니처', '셀픽스', '하루필름']);
const brand_dict = {"인생네컷": "lifefourcut", "포토이즘박스": "photoism", "포토시그니처": "photosignature", "셀픽스": "selfix", "하루필름": "harufilm"}


// 브랜드별 색깔 바꿀 때 이 부분 src 수정, 혹은 실제 pin 박을 때 수정도 가능
// 참고 -> 이 api에서는 href 링크나 실제 이미지로만 pin 이미지 설정 가능. <i> rexicon꺼 </i> 등 형태 불가. 
const imageSrc = '../static/icons/pin_blue.png'
const imageSize = new kakao.maps.Size(28, 28);
const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);  // 기본 파란 핀

const lifefourcutpin = new kakao.maps.MarkerImage('../static/icons/lifefourcuts.svg', imageSize)
const selfixpin = new kakao.maps.MarkerImage('../static/icons/selfix.svg', imageSize)
const photoismpin = new kakao.maps.MarkerImage('../static/icons/photoism.svg', imageSize)
const harufilmpin = new kakao.maps.MarkerImage('../static/icons/harufilm.svg', imageSize)
const photosignaturepin = new kakao.maps.MarkerImage('../static/icons/signature.svg', imageSize)
var brandpin = null;

// 지도에 표시된 마커 객체를 가지고 있을 배열입니다.
// 브랜드 별로 따로 생성해주었습니다.
for (let value in brand_dict){
    eval("var "+brand_dict[value]+"Markers"+" = []") 
};
// ex) var selfixMarkers = [];


// 클러스터링 객체 생성, minLevel 15로 절대 cluster 안되게
const clu = new kakao.maps.MarkerClusterer({map: map, averageCenter: true, minLevel: 15});

var bounds = map.getBounds(); // 지도 범위 가져오는 bounds 변수 초기값 생성

// 전역 변수 생성 끝 -----------------------------------------------------------------------------


// 3 현재 위치 찍기 -----------------------------------------------------------------------------

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

// 현재 위치 찍기 끝 -----------------------------------------------------------------------------


// 4 초기 부스 정보 다루기 -----------------------------------------------------------------------------

// 일단 render로 넘어온 모든 booth들 안보이게 boothList에 등록
var boothList = document.getElementById('boothList');
let total = boothList.childElementCount; // count booths    

// booth list하는 아코디언 dom
var accList = document.getElementById('accordionList')

// 범위 내의 booth list 저장해두는 array
let mapboundbooth = []

for (let i=0; i<total; i++) {
    setbooth(i);
    // 클러스터에 브랜드별 marker 배열 넣기
    for (let value in brand_dict){
        // let engbrand = brand_dict[value]
        clu.addMarkers(eval(brand_dict[value]+"Markers"))
        // ex) harufilmClust.addMarkers(harumfilmMarkers)
    };
}

function setbooth(i) {
    let booth = boothList.children[i] // 특정 booth 정보 담은 객체
    // let booth = boothparent.firstElementChild.dataset
    const name = booth.firstElementChild.dataset.name
    const brandname = booth.firstElementChild.dataset.brand
    
    
    const mapLat = booth.firstElementChild.dataset.x
    const mapLng = booth.firstElementChild.dataset.y
    var coords = new kakao.maps.LatLng(mapLat, mapLng)

    // 각자 브랜드에 맞는 pin icon 할당
    brandpin = eval(brand_dict[brandname]+"pin;")
    addMarker(coords, brandpin, infowindow, brandname);
    // 초기 607개 pin 배열 생성

    // 특정 pin's infowindow 설정
    var content = '<div style="padding:2px;z-index:1;font-size:8px; text-align: center!important;">' + name + '</div>';
    var infowindow = new kakao.maps.InfoWindow({zIndex:1}); // 새 info object
    infowindow.setContent(content); // infowindow 내용
    infowindow.setPosition(coords); // 인포윈도우 달릴 위치 설정 (=해당 핀 좌표)


    // booth의 좌표가 현재 지도 boundary 안에 있는거면 list up
    if (bounds.contain( coords )) {
        printList(booth); // list에 표시하기             
        mapboundbooth.push(booth);           
        // console.log("위치 안")
    }

}

function addMarker(pos, img, infowindow, brandname) {
    var marker = new kakao.maps.Marker({
        // map:map,
        position: pos,
        image: img,
    });
    // console.log(marker);
    marker.setMap(map);

    eval(brand_dict[brandname]+"Markers.push(marker);")
    // brand별로 marker 배열에 marker push
    
    setClickEvents(marker, infowindow);

}

// 리스트에 매장 추가
function printList(boothElement) {
    
    const brand = boothElement.firstElementChild.dataset.brand;

    if (!filterSet.has(brand)) {
        return 0;
    }

    // 지도 내에 있는 booth의 정보 가져오기
    let name = boothElement.firstElementChild.dataset.name;
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

// 초기 부스 정보 다루기 끝 -----------------------------------------------------------------------------


// 5 map 범위 달라졌을 때 -----------------------------------------------------------------------------
// 초기 세팅 이후, 화면 변경에 따라 list 표시 다르게

kakao.maps.event.addListener(map, 'center_changed', findList); // 중심 좌표 움직였을 때
kakao.maps.event.addListener(map, 'zoom_changed', findList); // 확대 축소 했을 때

// 바뀐 범위의 booth들 찾는 함수
function findList() {
    accList.innerHTML = '';
    // 이미 되어있던 acc 리스트 초기화
    mapboundbooth = []
    // 현재 범위 안의 booth들 담아놓는 객체도 초기화

    bounds = map.getBounds(); // 화면 변경되었으니 범위 다시 가져오고

    for (let i=0; i<total; i++) { // 모든 booth들 다시 탐색...
    
        let booth = boothList.children[i]
        let lat = booth.firstElementChild.dataset.x
        let lng = booth.firstElementChild.dataset.y
        let boothcoord = new kakao.maps.LatLng(lat, lng)
        
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

// map 범위 변경 다루기 끝 -----------------------------------------------------------------------------


// 6. 정렬 필터 -----------------------------------------------------------------------------
// 가나다순은 빼기로 했고, 거리순은 디폴트로 해둘 예정인데 아직 구현 전
// alphabet
var sortAlpha = document.getElementById('sortAlpha');
var sortAlphaDesc = document.getElementById('sortAlphaDesc');
var sortDist = document.getElementById('sortDist'); // 아직 구현 전

sortAlpha.addEventListener('click', function() {
    
    if (this.checked) {
        // console.log("checked!")

        mapboundbooth.sort(function(a, b) {
            var nameA = a.firstElementChild.dataset.name; // ignore upper and lowercase
            var nameB = b.firstElementChild.dataset.name; // ignore upper and lowercase
            if (nameA < nameB) { return -1; }
            if (nameA > nameB) { return 1; }
            return 0; // 이름이 같을 경우
        });

        accList.innerHTML = '';

        for (var index of mapboundbooth) {
            printList(index, accList);
        }
    }
});

sortAlphaDesc.addEventListener('click', function() {
    
    if (this.checked) {
        // console.log("desc checked!")

        mapboundbooth.sort(function(a, b) {
            var nameA = a.firstElementChild.dataset.name; // ignore upper and lowercase
            var nameB = b.firstElementChild.dataset.name; // ignore upper and lowercase
            if (nameA > nameB) { return -1; }
            if (nameA < nameB) { return 1; }
            return 0; // 이름이 같을 경우
        });

        accList.innerHTML = '';

        for (var index of mapboundbooth) {
            printList(index, accList);
        }
    }
});

// 거리순 정렬 아직 미구현. default로 할까 생각중.
// 정렬 필터 끝 -----------------------------------------------------------------------------


// 5. 브랜드 필터 -----------------------------------------------------------------------------
const filterLifefour = document.getElementById('filter-lifefour');
const filterPhotoism = document.getElementById('filter-photoism');
const filterSignature = document.getElementById('filter-signature');
const filterSelfix = document.getElementById('filter-selfix');
const filterHaru = document.getElementById('filter-haru');


const filterGroup = document.getElementById('filterGroup');

// 어떤 거든 필터 설정이 클릭되었을 때
filterGroup.addEventListener('click', function() {
    
    clu.clear()
    // 일단 맵에서 모든 pin들 제거
    accList.innerHTML = '';
    // 리스트도 초기화.

    for (let i=1; i<this.childElementCount; i=i+2) {
        brandname = this.children[i].innerHTML;

        if (this.children[i-1].checked) { // 필터가 체크되어있다면
            filterSet.add(brandname); // 필터 set에 해당 브랜드 등록. set이라 중복 x
            clu.addMarkers(eval(brand_dict[brandname]+"Markers"))
            // 클러스터에 해당 brand의 marker 객체들 다 등록!
            // ex) clu.addMarkers(harumlifmMarkers)
            // 그러면 하루필름 pin들이 다 map에 등록
        }
        else { // 필터가 체크되어있지 않다면
            filterSet.delete(brandname) // 필터 set에서 해당 브랜드 삭제.
            // 클러스터 등록 과정이 없어, 당연히 map에 pin이 박히지 않음. 처음에 다 삭제해줬기 때문.
        }
    } // filterSet은 listup할때 쓰일 예정!

    // 이 부분에서 style 바꾸는 건 그 클러스터 동그라미만 해당이 되는거라
    // pin들을 삭제하기 위해서는 marker 배열들을 cluster에 delete랑 add하면서 구현할수밖에 없었음.

    // 방식은 지금같은 전체 pin 삭제 -> 체크된 브랜드들만 pin 추가하는거 말고,
    // 전체가 다 박혀있는 상황에서 check 안된 브랜드들만 제거하는 방법도 있긴 함.
    // 삭제까지는 괜찮음.
    // 문제는 filter을 해제했다 다시 체크하면 check가 된 브랜드 pin들을 다시 cluster에 추가해줘야 하자나?
    // 근데 이때 맨 처음에 해제를 하나만 하니까 그러면 나머지 4개는 check된 상태인데
    // 그러면 원래 전체 pin들 + check된 4개 브랜드들 pin이 cluster에 추가될거고, 두번 pin들이 들어갈 거란 말이지? 
    // cluster가 set 형식으로 지원하는거면 모르겠는데 아닌 것 같아서...
    // 아니 글로 설명할라니까 못하겠어
    // 혹시 필요하면 회의 끝나고 설명해줄게....... 

    // 아래는 list 관련
    for (var booth of mapboundbooth) {
        // 이 printList할때 filterSet의 브랜드들 걸러서 listup 해줌!
        printList(booth);    
    }
    
});

// 브랜드 필터 끝 -----------------------------------------------------------------------------
