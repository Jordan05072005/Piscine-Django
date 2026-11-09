function scrollToBottom() {
    const box = $('#messages');
    box.scrollTop(box[0].scrollHeight);
}

$(function () {
    const roomName = JSON.parse(document.getElementById('room-name').textContent);
    const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${protocol}://${location.host}/ws/chat/${roomName}/`);
    scrollToBottom();

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        let p;
        switch (data.type) {
            case 'chat_message':
                data.messages.forEach(function (message, i) {
                    if (data.system[i]) {
                        p = $('<p class="system">').text(message);
                    } else {
                        p = $('<p>');
                        p.append($('<span class="author">').text(data.username[i] + ':'));
                        p.append(document.createTextNode(' ' + message));
                    }
                    $('#messages').append(p);
                });

                scrollToBottom();
                break;
            case 'connection':
                const list = $('#users').empty();
                const usernames = data.users
                const me = JSON.parse(document.getElementById('me').textContent);
                if (!usernames.length) {
                    list.append('<li class="empty">Personne pour l’instant</li>');
                    return;
                }
                usernames.forEach(function (name) {
                    const isMe = name === me;
                    const li = $('<li class="user">').toggleClass('me', isMe);
                    li.append(isMe
                        ? '<span class="star" aria-hidden="true">★</span>'
                        : '<span class="dot" aria-hidden="true"></span>');
                    li.append($('<span class="username">').text(name));
                    list.append(li);
                });
        }


    };

    socket.onclose = function () { // lorsque le connection socket est fermé
        $('#messages').append($('<p class="error">').text('Connection lost.'));
        scrollToBottom();
    };

    $('#disconnected').on('click', function (e) {
        // e.preventDefault();

        socket.close();
    });

    $('#chat-form').on('submit', function (e) {
        e.preventDefault();
        socket.send(JSON.stringify({ message: $('#chat-input').val() }));
        $('#chat-input').val('');
    });
});
