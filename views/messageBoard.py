mb_html = """
<!DOCTYPE html>
<html>
    <style>
        div.container {
          width:100%;
          overflow:auto;
        }
        ul.messages {
          outline-style: solid;
        }
        div.container div {
          width:33%;
          float:left;
        }
    </style>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <div class="container">
            <div>
                <p>User</p>
                <form action="" onsubmit="sendMessage(event)">
                    <input type="text" id="senderId" autocomplete="off" placeholder="user id" required=true/>
                    <input type="text" id="messageBoard" autocomplete="off" placeholder="board id" required=true/>
                    <input type="text" id="messageText" autocomplete="off" placeholder="text" required=true/>
                    <button>Send</button>
                </form>
            </div>
            <div>
                <p>Messages</p>
                <ul id='messages' class='messages'>
                    <li>Test message</li>
                </ul>
            </div>
        </div
    </body>
    <script>
        var id = "";
        var ws = new WebSocket("ws://localhost:8000/ws/chatServer");
        ws.onmessage = function(event) {
            var messages = document.getElementById('messages')
            var message = document.createElement('li')
            var content = document.createTextNode(event.data)
            message.appendChild(content)
            messages.appendChild(message)
        };
        function sendMessage(event) {
            var id = document.getElementById("senderId")
            var mboard = document.getElementById("messageBoard")
            var input = document.getElementById("messageText")
            var timestamp = new Date().toISOString().slice(0, 19);
            data = ""+mboard.value+","+id.value+","+input.value+","+timestamp;
            ws.send(data)
            input.value = ''
            event.preventDefault()
        };
    </script>
</html>
"""
