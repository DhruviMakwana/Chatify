function loginRedirect()
{
     window.location.href= '/login_page/';
}

    //NOTIFICATION FUNCTION

    function showNotification(message, fullname) {
        if (Notification.permission === "granted") {
            const options = {
                body: message,
//                icon: "https://picsum.photos/200/300"
                icon: 'http://127.0.0.1:8000/media/profile_photo/download_Ynsue9Q.jpeg'
            };
            new Notification("New Message From " + fullname, options);
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(function(permission) {
                if (permission === "granted") {
                    showNotification(message);
                }
            });
        }
    }