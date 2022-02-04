$(document).ready(function () {
    $("#cards-box").html("");
    showList();
});

function openClose() {
    // id 값 post-box의 display 값이 block 이면(= 눈에 보이면)
    if ($("#post-box").css("display") === "block") {
        // post-box를 가리고
        $("#post-box").hide();
        // 다시 버튼을 클릭하면, 박스 열기를 할 수 있게 텍스트 바꿔두기
        $("#btn-post-box").text("컴색 시작");
    } else {
        // 아니면(눈에 보이지 않으면) post-box를 펴라
        $("#post-box").show();
        // 다시 버튼을 클릭하면, 박스 닫기를 할 수 있게 텍스트 바꿔두기
        $("#btn-post-box").text("컴색 끝");
    }
}

function comsecPost() {
    let comsec = $("#post-url").val();
    $.ajax({
        type: "POST",
        url: "/comsec",
        data: {comsec_give: comsec},
        success: function (response) { // 성공하면
            if (response["result"] === "success") {
                alert("성공!")
                window.location.reload()
            }
        }
    })
}

function showList() {
    $.ajax({
        type: "GET",
        url: "/memo",
        data: {},
        success: function (response) {
            let articles = response["articles"];
            for (let i = 0; i < articles.length; i ++) {
                makeCard(articles[i]["img"], articles[i]["url"],articles[i]["title"],articles[i]["desc"])
            }
        }
    })
}

function makeCard(image, url, title, desc, comment) {
    let temp_html = `<div class="card">
                        <img class="card-img-top" src="${image}" alt="Card image cap">
                        <div class="card-body">
                        <a href="${url}" target="_blank" class="card-title">${title}</a>
                        <p class="card-text">${desc}</p>
                        </div>
                    </div>`;
    $("#cards-box").append(temp_html);
}