console.log("extension works (background)")

var session = ['screen', 'window'];

chrome.runtime.onConnect.addListener(function (port) {
    port.onMessage.addListener(portOnMessageHanlder);
    
    // this one is called for each message from "content-script.js"
    function portOnMessageHanlder(message) {
        if(message == 'get-sourceId') {
            chrome.desktopCapture.chooseDesktopMedia(session, port.sender.tab, onAccessApproved);
        }
    }

    // on getting sourceId
    // "sourceId" will be empty if permission is denied.
    function onAccessApproved(sourceId) {
        console.log('sourceId', sourceId);
        
        // if "cancel" button is clicked
        if(!sourceId || !sourceId.length) {
            return port.postMessage('PermissionDeniedError');
        }
        
        // "ok" button is clicked; share "sourceId" with the
        // content-script which will forward it to the webpage
        port.postMessage({
            sourceId: sourceId
        });
    }
});

// ws = new WebSocket("ws://localhost:8088");


// chrome.runtime.onConnect.addListener(function (port) {
//     port.onMessage.addListener(portOnMessageHanlder);
//     console.log("connected to chrome runtime")

//     function portOnMessageHanlder(message) {
//         if(message == 'get-sourceId') {
//             chrome.desktopCapture.chooseDesktopMedia(session, port.sender.tab, onAccessApproved);
//         }
//     }

//     // on getting sourceId
//     // "sourceId" will be empty if permission is denied.
//     function onAccessApproved(sourceId) {
//         console.log('sourceId', sourceId);
        
//         // if "cancel" button is clicked
//         if(!sourceId || !sourceId.length) {
//             return port.postMessage('PermissionDeniedError');
//         }
        
//         // "ok" button is clicked; share "sourceId" with the
//         // content-script which will forward it to the webpage
//         port.postMessage({
//             sourceId: sourceId
//         });
//     }

// })

// ws.onopen = function(){
//     console.log("connected to server") 
//     ws.send("hi")   
// }

// ws.onmessage = function(msg){
//     console.log("got message", msg)
// }


