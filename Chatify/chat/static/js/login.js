function login(e) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    e.preventDefault();
    var formdata = new FormData($('#login_form')[0]);
    makeAjaxRequest('POST', csrfToken, "/api/login/", formdata, function(response) {
        var login_err = JSON.parse(response.responseText).error
       
        if(login_err){
            $("#error").html(login_err);
        }
        else{
            window.location.href = '/chat/';
        }
    })
}

