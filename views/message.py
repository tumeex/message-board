m_html = """
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
                <p>Join</p>
                <form action="" onsubmit="sendMessage(event)">
                    <input type="text" id="name" autocomplete="off" placeholder="user name" required=true/>
                    <input type="text" id="mboard" autocomplete="off" placeholder="board id" required=true/>
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
        var ws = new WebSocket("ws://localhost:8000/ws/welcome");
        ws.onmessage = function(event) {
            var messages = document.getElementById('messages')
            var message = document.createElement('li')
            var content = document.createTextNode(event.data)
            message.appendChild(content)
            messages.appendChild(message)
        };
        function sendMessage(event) {
            event.preventDefault()
            var name = document.getElementById("name").value
            var mboard = document.getElementById("mboard").value
            ws.close()

            console.log("Data:", mboard, name);

            window.location.href = "http://127.0.0.1:8000/boards/join/" +
                                    encodeURIComponent(mboard) + "/" +
                                    encodeURIComponent(name);

        };
    </script>
</html>
"""
