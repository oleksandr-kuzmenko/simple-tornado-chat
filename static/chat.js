var ws = new WebSocket("ws://127.0.0.1:8000/chat");

ws.onmessage = function (evt) {
   $('#start').after('<p>' + evt.data + '</p>')
};

$('#msg_form').submit(function(){
    $msg = $("input[name='msg']").val()
    $("input[name='msg']").val('');
    ws.send($msg);
    return false;
});
