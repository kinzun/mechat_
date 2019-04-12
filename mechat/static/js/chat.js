function cur_time() {
    var myDate = new Date;
    var year = myDate.getFullYear(); //获取当前年
    var mon = myDate.getMonth() + 1; //获取当前月
    var date = myDate.getDate(); //获取当前日
    var h = myDate.getHours();//获取当前小时数(0-23)
    var m = myDate.getMinutes();//获取当前分钟数(0-59)
    var s = myDate.getSeconds();//获取当前秒
    var week = myDate.getDay();
    var weeks = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
    // console.log(year, mon, date, weeks[week])
    // {#$("#time").html(year + "年" + mon + "月" + date + "日" + weeks[week] + h + m + s);#}
    var cur_time_time = (year + "年" + mon + "月" + date + "日" + weeks[week] + h + ':' + m + ':' + s);
    return cur_time_time

};


var nickname = $('.nickname').val();
var ws = new WebSocket('ws://' + window.location.hostname + ':9999/chat');

ws.onopen = function () {
    $('.connecting_status').text('connected');
}

ws.onclose = function () {
    $('.connecting_status').text('disconnected');
}

ws.onmessage = function (msg_event) {
    var data = $.parseJSON(msg_event.data);

    // console.log(data);
    if (data.msg_type == 'message') {

        function info_add(head, mes) {
            $('.message_pane').append(
                '<div class="msg-box">' +
                '<div class="picture">' +
                '<img class="pop-card" data-position="right center" data-offset="-40" data-href="/profile/30"' +
                'src=' + head + '>' +
                '</div>' +
                '<div class="msg">' +
                '<span id="nickname2">' + mes.nickname + '</span>' +
                '<small class="timestamp"><span class="" ' +
                'style="">' + cur_time() + '</span>' +
                '</small>' +
                '<span class="message-body" id="message_re">' + mes.message + '</span>' +
                '</div>' +
                '</div>'
            )
            ;
            $('.message_pane').animate({scrollTop: $('.message_pane')[0].scrollHeight}, 1000);
        }

        // {msg_type: "message", nickname: "图灵机器人的爸爸", message: "嗯，怎么样"}
        if (data.the_robot == 'robot') {
            info_add("/static/jqm.jpg", data);
        } else {
            info_add("/static/huhu.jpg", data);
        }
    } else if (data.msg_type == 'update_clients') {
        $('.connected_clients li').remove();

        data.clients.forEach(function (nick) {
            $('.connected_clients').append('<li>' + nick);

        });
    }
}

setInterval(function () {
    ws.send(JSON.stringify({
        msg_type: 'update_clients',
        nickname: nickname
    }));
}, 2000);

$('.message').keypress(function (e) {
    if (e.which === 13) {
        $('.send_message').click();
    }
});


$('.send_message').click(function () {
    ws.send(JSON.stringify({
        msg_type: 'message',
        nickname: nickname,
        message: $('.message').val(),
        cur_time: cur_time()
    }));
    $('.message').val('');
});

$('.change_nickname').click(function () {
    nickname = $('.nickname').val();
});
