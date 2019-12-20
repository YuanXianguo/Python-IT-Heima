function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $("#form-avatar").submit(function (e) {
        e.preventDefault(); // 阻止表单的默认行为
        // 利用jquery.form.min.js提供的ajaxSubmit对表单进行异步提交
        $(this).ajaxSubmit({
            url: "/api/v1.0/users/avatar",
            type: "post",
            dataType: "json",
            headers:{
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (data) {
                if (data.errno == "0"){
                    var avatarUrl = data.data.avatar_url;
                    $("#user-avatar").attr("src", avatarUrl);
                }else{
                    alert(data.errmsg);
                }
            }
        })
    })

    $("#form-name").submit(function (e) {
        e.preventDefault();
        var name = $("#user-name").val();
        $.ajax({
            url: "/api/v1.0/users/name",
            type: "put",
            data: JSON.stringify({name: name}),
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (data) {
                if (data.errno == "0"){
                    $(".error-msg").hide();
                    showSuccessMsg();
                }else if (data.errno == "4103"){
                    $(".error-msg").show();
                }else{
                    alert(data.errmsg)
                }
            }
        })
    })
})
