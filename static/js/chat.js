document.getElementById('sendChat').addEventListener('click', function () {
    var input = document.getElementById('chatinput');
    var message = input.value;
    input.value = '';

    message = '<b>Você: </b>' + message;
    var chatbox = document.getElementById('chatbox');
    var userMessageEl = document.createElement('div');
    userMessageEl.setAttribute('class', 'user');

    userMessageEl.innerHTML = message;
    chatbox.appendChild(userMessageEl);

    var typingIndicator = document.createElement('div');
    typingIndicator.setAttribute('class', 'typing');
    typingIndicator.innerHTML = 'Assistente está digitando...';
    chatbox.appendChild(typingIndicator);

    fetch('/sendChat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: message }),
    })
    .then(response => response.json())
    .then(data => {
        var chatbox = document.getElementById('chatbox');
        chatbox.removeChild(typingIndicator);
        var newMessage = document.createElement('div');
        newMessage.setAttribute('class', 'system');
        newMessage.innerHTML = '<b>Assistente:</b>' + data.result;
        chatbox.appendChild(newMessage);
    });
});