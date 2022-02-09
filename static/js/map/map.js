// 지도 초기 설정
var container = document.getElementById('map');
var options = {
    center: new kakao.maps.LatLng(37.557074, 126.929276), // 임의의 중심 좌표
    level: 4 // 확대 축소 정도
};

var map = new kakao.maps.Map(container, options); // 지도 생성


// 지도 가장자리 꾸미기 관련 ------------------------------------------------------
// 지도 확대 축소를 제어할 수 있는  줌 컨트롤을 생성합니다
var zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.LEFT);

// 지도가 확대 또는 축소되면 마지막 파라미터로 넘어온 함수를 호출하도록 이벤트를 등록합니다
kakao.maps.event.addListener(map, 'zoom_changed', function() {        
    
    // 지도의 현재 레벨을 얻어옵니다
    var level = map.getLevel();
    
    var message = '현재 지도 레벨은 ' + level + ' 입니다';
    var resultDiv = document.getElementById('result');  
    resultDiv.innerHTML = message;
    
});


// blue pin으로 된 marker image 생성
var imageSrc = '../static/icons/pin_blue.png'
var imageSize = new kakao.maps.Size(32, 32);
var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 


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
    console.log("일단 이거 gps check 했고")

    if (navigator.geolocation) {
        console.log("이걸 안띄우?나?")
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
    console.log("Showlocation도 햇지?")
    console.log(gps_lat)
    console.log(gps_lng)

    var currentPosition  = new kakao.maps.LatLng(gps_lat,gps_lng); 
            
    var marker = new kakao.maps.Marker({  
        map: map, 
        position: currentPosition, 
        image: new kakao.maps.MarkerImage('../static/icons/pin_current.png', new kakao.maps.Size(24, 24))
    }); 

    marker.setMap(map);
    map.setCenter(currentPosition);      
    map.setLevel(7)
}


// error발생 시 에러의 종류를 알려주는 함수.
function errorHandler(error) {
    if(error.code == 1) {
        alert("위치 엑세스가 거부되었습니다.\n기본 위치로 이동합니다.");
    } else if( err.code == 2) {
        alert("위치를 반환할 수 없습니다.");
    }
    gps_use = false;
}



// 2 부스 위치 찍기 -----------------------------

// 주소 정보 가져오기
// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();


// 주소로 좌표를 검색합니다
var boothList = document.getElementById('boothList');
let total = boothList.childElementCount; // count booths    
// var infowindow = new kakao.maps.InfoWindow({zIndex:1});


var bounds = map.getBounds();
var accList = document.getElementById('accordionList')
// console.log(bounds.getSouthWest().toString())
// console.log(bounds.getNorthEast().toString())

async function for_pin(total){
    for (let i=0; i<total; i++) {
        var pin = await pinnn(i);
    }
}

for_pin(total);

function pinnn(i) {
    // const element = document.getElementById(`mapdetail-${i}`);
    let booth = boothList.children[i]
    let address = booth.firstElementChild.dataset.loc
    // console.log(address)
    if (address == "인천 미추홀구 숙골로87번길 5 5블럭 1층 40호") {
        // console.log("yes")
        address = "인천 미추홀구 숙골로87번길 5";
    }

    const name = booth.firstElementChild.dataset.name
    // console.log(name)
    // console.log(typeof name)
    
    var content = '<div style="padding:2px;z-index:1;font-size:8px; text-align: center!important;">' + name + '</div>';

    var infowindow = new kakao.maps.InfoWindow({zIndex:1});
    infowindow.setContent(content);

    geocoder.addressSearch(address, function(result, status) {
        // console.log(status)
        // 정상적으로 검색이 완료됐으면 
        if (status === kakao.maps.services.Status.OK) {
    
            var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

            // 경도 위도 값도 저장
            booth.firstElementChild.setAttribute('data-lat', coords.getLat())
            booth.firstElementChild.setAttribute('data-lng', coords.getLng())

            
            // 결과값으로 받은 위치를 마커로 표시합니다
            var marker = new kakao.maps.Marker({
                map: map,
                position: coords,
                image: markerImage
            });
            marker.setMap(map);
            // 지도에 핀은 일단 다 찍어놓기 

            
            infowindow.setPosition(coords);

            (function(marker, infowindow) { // 파라미터
                // 마커에 mouseover 이벤트를 등록하고 마우스 오버 시 인포윈도우를 표시합니다 
                kakao.maps.event.addListener(marker, 'mouseover', function() {
                    infowindow.open(map, marker);
                });
        
                // 마커에 mouseout 이벤트를 등록하고 마우스 아웃 시 인포윈도우를 닫습니다
                kakao.maps.event.addListener(marker, 'mouseout', function() {
                    infowindow.close();
                });

                // name_ele.onmouseover =  function () {
                //     infowindow.open(map, marker);
                // };

                // name_ele.onmouseout =  function () {
                //     infowindow.close();
                // };
                // console.log("set hover func");
            })(marker, infowindow); // 실제 넘기는거

            
            // 지도 boundary 안에 있는거만 list
            if (bounds.contain( coords )) {
                printList(booth, accList); // list 표시하기                
            }

            else {
                // console.log("not in map")
            }  
    
        }
        else {
            console.log("안돼?")
            console.log(result)
        }
    });

     // marker 위에 infowindow 표시하기
    return i;

}

// 중심 좌표 움직였을 때
kakao.maps.event.addListener(map, 'center_changed', findList);
// 확대 축소 했을 때
kakao.maps.event.addListener(map, 'zoom_changed', findList)


function findList() {
    accList.innerHTML = '';
    // acc 리스트 초기화

    var bounds = map.getBounds();

    for (let i=0; i<total; i++) {
    
        let booth = boothList.children[i]
        let lat = booth.firstElementChild.dataset.lat
        let lng = booth.firstElementChild.dataset.lng
        boothcoord = new kakao.maps.LatLng(lat, lng)
        
        if (bounds.contain( boothcoord )) {
            printList(booth, accList); // list 표시하기                
        }
    
        else {
            // console.log("not in map")
        }  
    }
}

function printList(boothElement, AccElement) {
    

    let name = boothElement.firstElementChild.dataset.name;
    let address = boothElement.firstElementChild.dataset.loc;
    const boothId = boothElement.id;
    const hour = boothElement.firstElementChild.dataset.hour;
    const brand = boothElement.firstElementChild.dataset.brand;

    const street = parseInt(boothElement.firstElementChild.dataset.street);
    const deco = parseInt(boothElement.firstElementChild.dataset.deco);
    const boxnum = parseInt(boothElement.firstElementChild.dataset.boxnum);
    const rating = parseFloat(boothElement.firstElementChild.dataset.rating);
    const likenum = boothElement.firstElementChild.dataset.likenum;

    // console.log(typeof street) // str
    // console.log(typeof likenum) // num
    // console.log(typeof hour) // str
    
    let streetContent = ''
    let decoContent = ''
    let hourContent = ''

    if (street) { streetContent = "매장점" }
    else { streetContent = "부스점" }

    if (deco) { decoContent = "○" }
    else { decoContent = "X" }

    if (hour) { hourContent = hour }



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

                    <a style="display: block;" class="mt-3" href="{% url 'map:detail' pk=${ boothId } %}">디테일페이지</a>
                </div>
            </div>
        </div>
    </div>`;

    AccElement.append(newdiv);
}

// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, name) {
    var content = '<div style="padding:5px;z-index:1;">' + name + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

// mouse hover event

