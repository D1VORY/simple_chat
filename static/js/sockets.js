const current_user = JSON.parse(document.getElementById('user_username').textContent);
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
);

// add outgoing message to DOM
function addOutgoingMsg(data, position = 'afterbegin'){
  let history =  document.querySelector('.msg_history')
  //console.log(history);
  history.insertAdjacentHTML(position,
    `<div class="outgoing_msg">
      <div class="sent_msg">
        <p>${data.text}</p>
        <span class="time_date">${data.timestamp}</span> </div>
    </div>`
   )
   // if it is called from websocket
   if (position == 'beforeend'){
      history.lastChild.scrollIntoView(false);
   }

}

// add incoming message to DOM
function addIncomingMsg(data, position = 'afterbegin') {
   let history =  document.querySelector('.msg_history')
   history.insertAdjacentHTML(position,
    `<div class="incoming_msg">
     <div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>
     <div class="received_msg">
         <div class="received_withd_msg">
           <p>${data.text}</p>
           <span class="time_date"> ${data.timestamp}</span></div>
     </div>
    </div>`
   )
   // if it is called from websocket
   if (position == 'beforeend'){
      history.lastChild.scrollIntoView(false);
   }
}

chatSocket.onmessage = function(e) {
   const data = JSON.parse(e.data);

   if (data.sender === current_user) {
     addOutgoingMsg(data,'beforeend')
   } else {
       addIncomingMsg(data,'beforeend')
   }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message){
      chatSocket.send(JSON.stringify({
          'message': message
      }));
      messageInputDom.value = '';
    }

};
