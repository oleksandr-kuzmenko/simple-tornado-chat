var ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onmessage = function (evt) {
    $('.table > tbody:last').append('<tr><td>' + evt.data + '</td></tr>');
    var n = $(document).height();
    $('html, body').animate({ scrollTop: n });
};

$('#msg_form').submit(function(){
    $msg = $("input[name='msg']").val()
    $("input[name='msg']").val('');
    ws.send($msg);
    return false;
});
