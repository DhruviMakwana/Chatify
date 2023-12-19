var app = angular.module('ChatApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
});

app.controller('chatCtrl', function($scope, $http) {
    $scope.userId = $('.userID').text();


    var ws = new WebSocket(`${scheme}//${url}/ws/chat/`)
    ws.onopen = function() {}

    $scope.removeOfflineUser = function(chat) {
        $scope.$apply(function() {
            $scope.chatData = $scope.chatData.filter(data => data.id != chat.id);
        });
    }

    $scope.addOnlineUserToList = function(userDetail) {
        if (!$scope.chatData.some(chat => chat.id == userDetail.id)) {
            $scope.$apply(function() {
                $scope.chatData.push(userDetail);
            });
        }
    };
    $scope.isBlocked = {}
    $scope.isBlockedText = {}
    $scope.blockMessageText = {}
    $scope.blockButtonText = {}

    ws.onmessage = function(e, ) {
        let userDetail = JSON.parse(e.data)
        $scope.bloke_user = userDetail.is_blocked

        if (userDetail.is_blocked == "true") {
            $scope.$apply(function() {

                $scope.chatData.forEach(function(item) {
                    if (item.id == userDetail.blocked_user || item.id == userDetail.blocked_by) {

                        $scope.isBlocked[userDetail.blocked_user] = true;
                        $scope.isBlocked[userDetail.blocked_by] = true;
                        $scope.blockButtonText[userDetail.blocked_user] = "Unblock";
                        $scope.isBlockedText[userDetail.blocked_user] = false;
                        $scope.isBlockedText[userDetail.blocked_by] = false;
                        $scope.blockMessageText[userDetail.blocked_user] = 'You are blocked.';
                    }
                });
            });
        } else if (userDetail.is_blocked == "false") {
            $scope.$apply(function() {
                $scope.chatData.forEach(function(item) {
                    if (userDetail.blocked_user == item.id || item.id == userDetail.blocked_by) {
                        $scope.isBlocked[userDetail.blocked_user] = false;
                        $scope.isBlocked[userDetail.blocked_by] = false;
                        $scope.blockButtonText[userDetail.blocked_user] = "block";
                        $scope.isBlockedText[userDetail.blocked_user] = true;
                        $scope.isBlockedText[userDetail.blocked_by] = true;
                        $scope.blockMessageText = "";
                    }
                });
            });
        } else if (userDetail.user_auth == "logout") {
            loginRedirect()
        } else if (userDetail.data.status == "offline") {
            $scope.removeOfflineUser(userDetail.data);
        } else if (userDetail.data.status == "online") {
            if (userDetail.data.id != $scope.userId) {
                $scope.addOnlineUserToList(userDetail.data);
            }
        }
    }

    ws.onclose = function(event) {}

    $scope.currentUser = undefined;
    $scope.status = 'online';

    $scope.ajaxGet = function(url, callback = null) {
        $http.get(url).then(function(response) {
            if (callback) {
                callback(response)
            }
        });
    }
    $scope.chatData = []

    $scope.ajaxGet('api/get_online_user/', function(response) {
        $scope.chatData = response.data.UserData;
    })

    $scope.chatData.forEach(function(item) {
        if (item.block_user == true) {
            $scope.isBlocked[item.id] = true;
            $scope.isBlocked[item.id] = true;
            $scope.blockButtonText[item.id] = "Unblock";
            $scope.isBlockedText[item.id] = false;
            $scope.isBlockedText[item.id] = false;
            $scope.blockMessageText[item.id] = 'You are blocked.';
        } else {

            $scope.isBlocked[item.id] = false;
            $scope.blockButtonText[item.id] = "block";
            $scope.isBlockedText[item.id] = true;
            $scope.isBlockedText[item.id] = true;
            $scope.blockMessageText = '';

        }
    });

    $scope.showChat = function(user) {
        if (!user.is_websocket_registered) {
            $scope.ps = new WebSocket(`ws://127.0.0.1:8000/ws/chat/message/${user.id}/`)
            $scope.ps.onopen = function() {}
            $scope.ajaxGet('api/messages/' + user.id, function(response) {
                $scope.data = response.data.messageData;
            })
            $scope.ps.onmessage = function(event) {
                response = JSON.parse(event.data)
                $scope.$apply(function() {
                    $scope.data.push(response)
                    showNotification(response.message, response.full_name);
                })
            }
        }
        user.is_websocket_registered = true
        $scope.currentUser = user

    };
    $scope.msgText = {};
    //   sending a chat on click button

    $scope.sendChat = function(user) {
        var message = $scope.msgText[user];
        $scope.msgText[user] = ""
        $scope.date = moment().format('DD/MM/YYYY, hh:mm:ss a');
        $scope.tz = Intl.DateTimeFormat().resolvedOptions().timeZone
        var file = $scope.fileInput ? $scope.fileInput.files[0] : $('input[type=file]')[0].files[0];
        if (file) {
            var formData = new FormData();
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            formData.append('receiverId', user)
            formData.append('senderId', $scope.userId)
            formData.append('date', $scope.date)
            formData.append('timezone', $scope.tz)
            formData.append('file', file)
            makeAjaxRequest('POST', csrfToken, "/api/savefile/", formData, function(response) {
                $scope.ps.send(JSON.stringify({
                    'msg': null,
                    'receiverId': user,
                    'senderId': $scope.userId,
                    'date': $scope.date,
                    'timezone': $scope.tz
                })); //$scope.fileInput = null; // Reset file input
                $('input[type=file]').val(null);
            })
        } else {
            $scope.ps.send(JSON.stringify({
                'msg': message,
                'receiverId': user,
                'senderId': $scope.userId,
                'date': $scope.date,
                'timezone': $scope.tz
            }))
        }
        var currentUser = $scope.chatData.find(function(u) {
            return u.id == user;
        });
    }

    $scope.handleFileDrop = function(files) {
        if (files && files.length > 0) {
            $scope.fileInput = files[0];
        }
    };

    // set status of user online/offline on radio button click
    $scope.setStatus = function(status, csrf_token, currentUser_id) {
        $scope.status = status;
        $scope.id = currentUser_id
        var formData = new FormData();
        formData.append('status', $scope.status)
        formData.append('id', $scope.id)
        makeAjaxRequest('POST', csrf_token, "/api/visibility-status/", formData, function(response) {

        })
    }

    $scope.addToBLockList = function(csrf_token, blockUserId) {
        var formData = new FormData();
        $scope.blocked = true
        formData.append('blockUserId', blockUserId)
        $scope.blockButtonText[blockUserId] = "block";
        makeAjaxRequest('POST', csrf_token, "api/block-user/", formData, function(response) {})
    }

    $scope.exportChat = function(currentUser_id) {
        current_user_id = currentUser_id
        $scope.ajaxGet('pdf_download/' + current_user_id, function(response) {
            var blob = new Blob([response]);
            var downloadUrl = URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = downloadUrl;
            a.download = "chat.pdf";
            document.body.appendChild(a);
            a.click();
        });
    }

    $scope.unsendMsg = function(csrf_token, UserId, currentUser, msg, msgid, sent_time) {
        var sentTime = moment(sent_time, "DD/MM/YYYY, hh:mm:ss a").format("YYYY-MM-DDTHH:mm:ssZ");
        var currentTime = new Date();
        var timeDiff = currentTime - new Date(sentTime);
        var formData = new FormData();
        formData.append('requestUser', UserId)
        formData.append('currentUser', currentUser)
        formData.append('message', msg)

        if (timeDiff < 60000) {
            makeAjaxRequest('POST', csrf_token, "/api/unsend-message/", formData, function(response) {})
            $scope.data = $scope.data.filter(data => data.message_id !== msgid);
        } else {
            alert("you can't unsend this message")
        }
    }
});