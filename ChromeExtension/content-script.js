// this content-script plays role of medium to publish/subscribe messages from webpage to the background script

ws = new WebSocket("ws://localhost:8088");
ws.onopen = function() {
    console.log("connected to server dawg")
}

ws.onmessage = function(msg) {
    console.log("got message", msg)
}

function startStreamFrom(sourceId) {
    navigator.webkitGetUserMedia({
            audio: false,
            video: {
                mandatory: {
                    chromeMediaSource: 'desktop',
                    chromeMediaSourceId: sourceId,
                    maxWidth: 320,
                    maxHeight: 240
                }
            }
        },
        // successCallback
        function(screenStream, something, another) {
            var url = URL.createObjectURL(screenStream);
            var video = document.createElement('video');
            // video.style.visible = 'none'
            var array = [];
            var canvas = document.createElement('canvas');
            // canvas.style.visible = 'none'
            var ctx = canvas.getContext('2d');

            video.autoplay = true;
            video.muted = true;

            video.addEventListener('loadedmetadata', function() {
                canvas.width = this.videoWidth;
                canvas.height = this.videoHeight;
            }, false);

            video.src = url;

            setInterval(function(){
                console.log("are you still there?")
                ctx.drawImage(video, 0, 0);
                data = canvas.toDataURL();
                // // data = data.replace(/^data:image\/(png|jpg);base64,/, "");
                ws.send(data); // this is the actual data, supposedly

            }, 100)

            // video.addEventListener('timeupdate', function() {
            //     this.pause(); // should be useless
            //     ctx.drawImage(this, 0, 0);
            //     data = canvas.toDataURL();
            //     // data = data.replace(/^data:image\/(png|jpg);base64,/, "");
            //     ws.send(data); // this is the actual data, supposedly
                
            //     if (this.duration > this.currentTime)
            //         this.play(); // should be useless
            // }, false);
///
            // video.addEventListener('ended', function() {
            // }, false);

        },
        function(err, huh, whatever) {
            console.log("error!", err)
        });
}

// this port connects with background script
port = chrome.runtime.connect();

// we expect the background script to send frames constantly

// got a message from the background script
port.onMessage.addListener(function(message) {
    // it's probably a frame
    // send it over the websocket to the server
    console.log("got some data from the background script")
    startStreamFrom(message['sourceId'])
    navigator.webkitGetUserMedia(message['sourceId'])
        // ws.send(message['sourceId'])
});


// this event handler watches for messages sent from the webpage
// it receives those messages and forwards to background script
window.addEventListener('message', function(event) {
    // if invalid source
    if (event.source != window)
        return;

    // if browser is asking whether extension is available
    if (event.data == 'are-you-there') {
        return window.postMessage('rtcmulticonnection-extension-loaded', '*');
    }

    // if it is something that need to be shared with background script
    if (event.data == 'get-sourceId') {
        // forward message to background script
        port.postMessage(event.data);
    }
});

// inform browser that you're available!
window.postMessage('rtcmulticonnection-extension-loaded', '*');