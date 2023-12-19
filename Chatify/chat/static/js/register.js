function register(e) {
        e.preventDefault();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var formdata = new FormData($('#register_form')[0]);
        makeAjaxRequest('POST', csrfToken, "/api/register/", formdata, function (response) {
                if (!response.responseText) {
                        loginRedirect()
                }
                else {
                        var error = JSON.parse(response.responseText).errors;
                        var username_err = JSON.parse(response.responseText).errors.username;
                        var number = JSON.parse(response.responseText).errors.mobile_number;
                        var pass_error = JSON.parse(response.responseText).errors.password;
                        var mail_error = JSON.parse(response.responseText).errors.email;
                        var profile_error = JSON.parse(response.responseText).errors.profile_photo;
                        $("#username").html(username_err);
                        $("#phonenumber").html(number);
                        $("#password").html(pass_error);
                        $("#confirm_password").html(pass_error);
                        $("#email").html(mail_error);
                        $("#profileerror").html(profile_error);
                }
        })
}

