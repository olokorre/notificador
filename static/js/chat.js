var socket;

$(document).ready(function(){
    socket = io();
    socket.on('connect', function() {
        socket.emit('joined', { room: 'main_room' });
    });
    socket.on('status', function(data) {
        $('#chat').val('');
        $('#chat').val($('#chat').val() + data.msg);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        var time = Date.now()
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#text').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text});
        }
    });
});

function clean_input(name) { document.getElementsByName(name).value = ''; }