function makeAjaxRequest(methodType, csrfToken, url, data, callback)
{
    $.ajax({
        method: methodType,
        headers: {
            'X-CSRFToken': csrfToken
        },
        url: url,
        data: data,
        contentType: false,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        error: function (data) {
             if (callback) {
                callback(data)
            }
        },

        cache: false,
        contentType: false,
        processData: false
    });
}

function ajaxGet(methodType, url, callback) {
    $.ajax({
        method: methodType,
        url: url,
        contentType: false,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        cache: false,
        contentType: false,
        processData: false
    });
}

