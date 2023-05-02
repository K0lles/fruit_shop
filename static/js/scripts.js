// Sets for chat socket onmessage event for adding new messages to message list
function set_onmessage_chat() {
    chatSocket.onmessage = function (event) {
        let server_answer = JSON.parse(event.data);
        let messages_div = $('.chat-messages');
        if (server_answer['start_connection']) {
            messages_div.empty();
            for (let message of server_answer['messages']) {
                messages_div.append(`<p>${message["formatted_date"]} ${message["user__username"]}: ${message["text"]}</p>`);
            }
        }
        else {
            if (server_answer.detail === 'error') toastr.error(server_answer["error_message"], 'Помилка');

            if (server_answer.detail === 'success') {
                messages_div.append(`<p>${server_answer["message"]["formatted_date"]} ${server_answer["message"]["user__username"]}: ${server_answer["message"]["text"]}</p>`);
            }
        }
    }
}

// Delete from header logout form and added there login
function changeToLoginForm() {
    let header_list = $('#header-list');
    header_list.empty();
    header_list.append(
        `<li class="nav-item">
            <input type="text" placeholder="Username" id="id_username" name="username" class="form-control">
         </li>
         <li class="nav-item">
             <input type="password" placeholder="Password" id="id_password" name="password" class="form-control">
         </li>
         <li>
             <button id="login-button" type="button" class="btn btn-success" onclick="login()">Login</button>
         </li>`
    );
    reconnect_websocket();
}

// Delete from header login form and added there logout button with display of username
function changeToLogoutForm(username) {
    let header_list = $('#header-list');
    header_list.empty();
    header_list.append(
        `<li class="nav-item">
            <p>${username}</p>
         </li>
         <li class="nav-item">
             <button type="button" id="logout-button" class="btn btn-danger" onclick="logout()">Logout</button>
         </li>`
    )
    reconnect_websocket();
}

function login() {
    let username = $('#id_username').val();
    let password = $('#id_password').val();
    $.ajax('/auth/login/', {
        type: 'POST',
        headers: {'X-CSRFToken': Cookies.get('csrftoken')},
        data: {'username': username, 'password': password},
        success: function(data) {
            if (data.detail === 'success') {
                Cookies.set('sessionid', data.request_session);
                changeToLogoutForm(data.username);
            }
            else {
                toastr.error(data.message, 'Помилка');
            }
        }
    })
}

function logout() {
    $.ajax('/auth/logout/', {
        type: 'GET',
        success: function(data) {
            if (data.detail === 'success') {
                Cookies.remove('sessionid');
                changeToLoginForm();
            }
            else {
                toastr.error(data.message, 'Помилка');
            }
        }
    })
}

// Reconnects to the WebSocket (used after login or logout)
function reconnect_websocket() {
    chatSocket.close();
    chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');
    set_onmessage_chat();
}
