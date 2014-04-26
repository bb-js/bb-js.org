
define(function(require, exports, module) {
    var $ = require('jquery');
    WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    WEB_SOCKET_DEBUG = true;

    var socket = io.connect();
    socket.on('connect', function(){
        console.log('connected');
    });

    socket.on('online_users', function(online_users){
        $('#online_users').empty().append($('<span>Online: </span>'));
        for (var i in online_users) {
            $('#online_users').append($('<span class="badge">').text(online_users[i].username));
        }
    });

    $(window).bind("beforeunload", function() {
        socket.disconnect();
    });
    return socket;
});
