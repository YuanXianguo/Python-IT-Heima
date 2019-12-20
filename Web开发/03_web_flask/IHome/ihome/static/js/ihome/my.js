function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function logout() {
    $.ajax({
        url: "/api/v1.0/session",
        type: "delete",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        dataType: "json",
        success: function (data) {
            if (data.errno == "0"){
                location.href = "/index.html"
            }
        }
    })
}

$(document).ready(function(){
    $.get("/api/v1.0/user", function (data) {
        if (data.errno == "0"){
            $("#user-avatar").attr("src", data.data.avatar_url);
            $("#user-name").html(data.data.name);
            $("#user-mobile").html(data.data.mobile);
        }
    })
})
