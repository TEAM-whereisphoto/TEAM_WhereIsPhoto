
// 1. 지도 자체 초기 설정 -----------------------------------------------------------------------------
var container = document.getElementById('map');
var defaultLoc = new kakao.maps.LatLng(37.557074, 126.929276)
var options = {
    center: defaultLoc, // 임의의 중심 좌표
    level: 4 // 확대 축소 정도
};
var map = new kakao.maps.Map(container, options); // 지도 생성
// 지도 확대 축소 컨트롤 생성
var zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

container.children[container.childElementCount-2].remove()

// 지도 자체 초기 설정 끝 -----------------------------------------------------------------------------


// 2 현재 위치 찍기 -----------------------------------------------------------------------------
    
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
    map.setCenter(currentPosition); // 내 위치를 중심 좌표로 이동
            
    var marker = new kakao.maps.Marker({  
        map: map, 
        position: currentPosition, 
        image: new kakao.maps.MarkerImage('../../static/icons/pin_current.png', new kakao.maps.Size(24, 24))
        // 현재 위치는 빨간색 pin_current로 이미지 설정해둠
    }); 

    marker.setMap(map); // 내 위치 pin 박기
    map.setLevel(7);
}


// error발생 시 에러의 종류를 알려주는 함수.
function errorHandler(error) {
    if(error.code == 1) {
        alert("위치 엑세스가 거부되었습니다.\n기본 위치로 이동합니다.");
        map.setLevel(4);
        map.panTo(defaultLoc);
    } else if( err.code == 2) {
        alert("위치를 반환할 수 없습니다.");
    }
    gps_use = false;
}

// 현재 위치 찍기 끝 -----------------------------------------------------------------------------
    

// 3. 전역 변수들 생성 -----------------------------------------------------------------------------

// 표시할 brand 이름. 나중에 brand model에서 가져오도록 수정해두면 더 좋긴 할듯.
const filterSet = new Set(['인생네컷', '포토이즘박스', '포토시그니처', '셀픽스', '하루필름']);
const brand_dict = {"인생네컷": "lifefourcut", "포토이즘박스": "photoism", "포토시그니처": "photosignature", "셀픽스": "selfix", "하루필름": "harufilm"}


// 브랜드별 색깔 바꿀 때 이 부분 src 수정, 혹은 실제 pin 박을 때 수정도 가능
// 참고 -> 이 api에서는 href 링크나 실제 이미지로만 pin 이미지 설정 가능. <i> rexicon꺼 </i> 등 형태 불가. 
const imageSrc = '../../static/icons/pin_blue.png'
const imageSize = new kakao.maps.Size(28, 28);
const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);  // 기본 파란 핀

const clickSize = new kakao.maps.Size(36, 36);
var selectedMarker = null; // 클릭한 마커를 담을 변수

for (let value in brand_dict){
    var key = brand_dict[value]
    
    // 브랜드별 icon 위치 src입니다.
    eval("var "+key+"Src"+"= '../../static/icons/"+key+".svg'") 
    
    // 지도에 표시된 마커 객체를 가지고 있을 배열입니다.
    // 브랜드 별로 따로 생성해주었습니다.
    // ex) var selfixMarkers = [];
    eval("var "+key+"Markers"+" = []")
}; 


const lifefourcutpin = new kakao.maps.MarkerImage(lifefourcutSrc, imageSize)
const selfixpin = new kakao.maps.MarkerImage(selfixSrc, imageSize)
const photoismpin = new kakao.maps.MarkerImage(photoismSrc, imageSize)
const harufilmpin = new kakao.maps.MarkerImage(harufilmSrc, imageSize)
const photosignaturepin = new kakao.maps.MarkerImage(photosignatureSrc, imageSize)
var brandpin = null;

const lifefourcutClick = new kakao.maps.MarkerImage(lifefourcutSrc, clickSize)
const selfixClick= new kakao.maps.MarkerImage(selfixSrc, clickSize)
const photoismClick = new kakao.maps.MarkerImage(photoismSrc, clickSize)
const harufilmClick = new kakao.maps.MarkerImage(harufilmSrc, clickSize)
const photosignatureClick = new kakao.maps.MarkerImage(photosignatureSrc, clickSize)



// 클러스터링 객체 생성, minLevel 15로 절대 cluster 안되게
const clu = new kakao.maps.MarkerClusterer({map: map, averageCenter: true, minLevel: 15});

var bounds = map.getBounds(); // 지도 범위 가져오는 bounds 변수 초기값 생성

// booth list하는 아코디언 dom
const boothListDom = document.getElementById('booth-list')

// 범위 내의 booth list 저장해두는 array
let mapboundbooth = []

const refresh = document.getElementById('refresh')

// 전역 변수 생성 끝 -----------------------------------------------------------------------------


document.addEventListener('DOMContentLoaded', function(){
    fetch('load/')
    .then( response => {
        return response.json()
    })
    .then(data => {
        main(data['boothList'])
    })
    .catch(error => {
        console.log("err", error)
    })
})

function main(boothList){ 

    // 4 초기 부스 정보 다루기 ----------------------------------------------------------------------------

    const total = boothList.length; // count booths    

    handleData();
    
    function handleData() {
        for (let i=0; i<total; i++) {
            setbooth(i);
        }
        // 클러스터에 브랜드별 marker 배열 넣기
        for (let value in brand_dict){
            // let engbrand = brand_dict[value]
            clu.addMarkers(eval(brand_dict[value]+"Markers"))
            // ex) harufilmClust.addMarkers(harumfilmMarkers)
        };       
    } 
    
    function setbooth(i) {
        let booth = boothList[i] // 특정 booth 정보 담은 객체
        // let booth = boothparent.firstElementChild.dataset
        const name = booth["name"]
        const brandname = booth["brand__name"]
        
        // 각자 브랜드에 맞는 pin icon 할당
        brandpin = eval(brand_dict[brandname]+"pin;")

        const mapLat = booth["x"]
        const mapLng = booth["y"]
        var coords = new kakao.maps.LatLng(mapLat, mapLng)
    
        addPin(coords, brandpin, brandname);
        // 초기 607개 pin 배열 생성
    
        // booth의 좌표가 현재 지도 boundary 안에 있는거면 배열에 push
        if (bounds.contain( coords )) { mapboundbooth.push(booth); }// console.log("위치 안")

    }


    function addPin(pos, img, brandname) {
        var marker = new kakao.maps.Marker({
            // map:map,
            position: pos,
            image: img,
        });
        // console.log(marker);
        marker.setMap(map);
        marker.normalImage = img;

        eval(brand_dict[brandname]+"Markers.push(marker);")
        // brand별로 marker 배열에 marker push
        
        setClickEvents(marker, brandname);
    }
    
    function setClickEvents (marker, brandname) {

        kakao.maps.event.addListener(marker, 'click', function() {
            // 클릭된 마커가 없고, click 마커가 클릭된 마커가 아니면
            // 마커의 이미지를 클릭 이미지로 변경합니다
            if (!selectedMarker || selectedMarker !== marker) {

                // 클릭된 마커 객체가 null이 아니면
                // 클릭된 마커의 이미지를 기본 이미지로 변경하고
                !!selectedMarker && selectedMarker.setImage(selectedMarker.normalImage);

                // 현재 클릭된 마커의 이미지는 클릭 이미지로 변경합니다
                marker.setImage( eval(brand_dict[brandname]+"Click") );
            }

            // 클릭된 마커를 현재 클릭된 마커 객체로 설정합니다
            selectedMarker = marker;

        })
    };

    // 초기 부스 정보 다루기 끝 -----------------------------------------------------------------------------
    
    
    // 5 map 범위 달라졌을 때 -----------------------------------------------------------------------------
    // 초기 세팅 이후, 화면 변경에 따라 list 표시 다르게
    
    kakao.maps.event.addListener(map, 'bounds_changed', findBoundBooth);
    
    // 바뀐 범위의 booth들 찾는 함수
    function findBoundBooth() {

        mapboundbooth = []
        // 현재 범위 안의 booth들 담아놓는 객체 초기화
    
        bounds = map.getBounds(); // 화면 변경되었으니 범위 다시 가져오고
    
        for (let i=0; i<total; i++) { // 모든 booth들 다시 탐색...
        
            let booth = boothList[i]
            let lat = booth["x"]
            let lng = booth["y"]
            let boothcoord = new kakao.maps.LatLng(lat, lng)
            
            // booth의 좌표가 현재 지도 boundary 안에 있는거면 list
            if (bounds.contain( boothcoord )) { mapboundbooth.push(booth) }
        }
    }
    
    // map 범위 변경 다루기 끝 -----------------------------------------------------------------------------
    
    
    // 7. 브랜드 필터 -----------------------------------------------------------------------------
    const filterGroup = document.getElementById('filterGroup');
    
    // 어떤 거든 필터 설정이 클릭되었을 때
    filterGroup.addEventListener('click', function() {
        
        clu.clear()
        // 일단 맵에서 모든 pin들 제거
    
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
    
    });
    
    // 브랜드 필터 끝 -----------------------------------------------------------------------------
    
    
    // 8. 검색했을 때 해당 지역으로 지도 이동 -----------------------------------------------------------------------------
    
    // 장소 검색 객체를 생성합니다
    var ps = new kakao.maps.services.Places(); 
    
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    
    searchBtn.addEventListener('click', function() {
        var keyword = searchInput.value
    
        // 키워드로 장소를 검색합니다
        ps.keywordSearch(keyword, placesSearchCB); 
    
        // 키워드 검색 완료 시 호출되는 콜백함수 입니다
        function placesSearchCB (data, status) {
            if (status === kakao.maps.services.Status.OK) {
    
                var newcenter = new kakao.maps.LatLng(data[0].y, data[0].x);
    
                // 검색된 장소들 중 첫번째꺼의 위치를 기준으로 지도 중심을 재설정합니다
                map.setCenter(newcenter);
                map.setLevel(6);
            }
            else if (status === kakao.maps.services.Status.ZERO_RESULT) {
                alert("입력된 장소가 없습니다. 다시 입력해주세요!")
            } 
    
            else {
                alert("검색 api에서 오류가 발생했습니다. 다시 검색해주세요!")
            }
        }
        searchInput.value = ''
    });

    searchInput.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.key === 'Enter') {
            event.preventDefault(); // 새로고침 방지
            // Trigger the button element with a click
            searchBtn.click();
        }
    });

    // 검색 끝 -----------------------------------------------------------------------------


    // 9. 내 위치 새로고침 -----------------------------------------------------------------------------

    refresh.addEventListener('click', function() {
        console.log("refresh")
        gps_check();
    });

    // 내 위치 새로고침 끝 -----------------------------------------------------------------------------


    // 10. 목록 보여주는 부분 -----------------------------------------------------------------------------

    // 목록 리스트에 매장 추가하는 함수
    function printList(boothElement) {
        
        const brand = boothElement["brand__name"];
    
        if (!filterSet.has(brand)) {
            return 0;
        }
    
        // 지도 내에 있는 booth의 정보 가져오기
        let name = boothElement["name"];
        let address = boothElement["location"];
        const boothId = boothElement["pk"];
        const hour = boothElement["operationHour"];
            
        const rating = boothElement["rating"];
        const reviewnum = boothElement["review_number"];
        var distance = Math.round(boothElement["len"])

        if ( distance < 1000 ) {
            distance = String(distance)+"m"
        }
        else {
            distance = Math.round(distance / 100) // ex) 5432 -> 54
            distance = String(distance / 10)+"km"
        }
        
        let hourContent = ''
        if (hour) { hourContent = hour } // 시간 null 아닌 경우만 표시
        var pinsrc = eval(brand_dict[brand]+"Src")

        const newdiv = document.createElement('div');
        newdiv.innerHTML = 
        `<div id="list-${ boothId }">
            <img style="width: 24px; margin-right: 5px" src=${ pinsrc }></img>${ name }

            <p style="margin: 16px 0 0 0">${distance} | ${ address }</p>

            <p style="margin: 16px 0 0 0"></p>
            ${ hourContent }
            </p>

            <button class="btn btn-outline-ratingNlike container" style="width: 75%;">
                <div class="row">

                    <div class = "col" style="color: #FFD107;">★ ${ rating }</div>
                    | 
                    <div class = "col" style="color: #484848"> ${ reviewnum } review(s) </div>  
                </div>
            </button>
    
            <a style="display: block;" class="mt-3" href="/find/booth/detail/${ boothId }">디테일페이지</a>
            <hr />
        </div>`;
    
        boothListDom.append(newdiv); // list추가
    }

    var curCenter = map.getCenter();

    const sorting = function sortDist(a, b) { // 거리순 정렬

        const coordA = new kakao.maps.LatLng(a["x"], a["y"]);
        const coordB = new kakao.maps.LatLng(b["x"], b["y"]);
        

        var polylineA = new kakao.maps.Polyline({
            map: map,
            path: [ coordA, curCenter ],
            strokeWeight: 0,
        });
        
        var polylineB = new kakao.maps.Polyline({
            map: map,
            path: [ coordB, curCenter ],
            strokeWeight: 0,
        });
        
        const lenA = polylineA.getLength();
        const lenB = polylineB.getLength();

        a['len'] = lenA
        b['len'] = lenB

        if (lenA < lenB) { return -1; }
        if (lenA > lenB) { return 1; }
        return 0; // 이름이 같을 경우
    }

    const listBtn = document.getElementById('list-btn');
    listBtn.addEventListener('click', function() {
        boothListDom.innerHTML='' // 이전에 만들어져있던게 있다면 초기화

        curCenter = map.getCenter()
        mapboundbooth.sort(sorting) // 거리순 정렬
        for (let booth of mapboundbooth){ printList(booth); } // list에 표시하기             
    }); 

    // 목록 끝 -----------------------------------------------------------------------------

}

