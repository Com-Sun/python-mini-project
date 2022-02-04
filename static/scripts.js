$(document).ready(function () {
    $("#cards-box").html("");
    comsecRead();
});

function openClose() {
    if ($("#post-box").css("display") === "block") {
        $("#post-box").hide();
        $("#btn-post-box").text("컴색 시작");
    } else {
        $("#post-box").show();
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

function comsecRead() {
    $.ajax({
        type: "GET",
        url: "/comsec",
        data: {},
        success: function (response) {
            let card = response["card"];
            for (let i = 0; i < card.length; i ++) {
                makeCard(card[i]["img"], card[i]["link"],card[i]["title"],card[i]["desc"])
            }
        }
    })
}

function makeCard(image, url, title, desc) {
    let temp_html = `<div class="card">
                        <img class="card-img-top" src="${image}" alt="Card image cap">
                        <div class="card-body">
                        <a href="${url}" target="_blank" class="card-title">${title}</a>
                        <p class="card-text">${desc}</p>
                        </div>
                    </div>`;
    $("#cards-box").append(temp_html);
}

function deleteDB(){
    $.ajax({
        type: "GET",
        url: "/comsec/delete",
        data: {},
        success: function (response) {
            if (response["result"] === "success") {
                alert("DB가 삭제되었소!")
                window.location.reload()
            }
        }
    })
}