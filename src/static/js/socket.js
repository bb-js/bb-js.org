
define(function(require, exports, module) {
    WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    WEB_SOCKET_DEBUG = true;

    var socket = io.connect();
    socket.on('connect', function(){
        console.log('connected');
    });

    $(window).bind("beforeunload", function() {
        socket.disconnect();
    });
    return socket;
});
