chrome.tabs.getSelected(null, function(tab) {
  // Send a request to the content script.
  chrome.tabs.sendMessage(tab.id, {message: "getInfo"}, function(response) {
    document.getElementById('articleName').innerHTML = "Wikipedia Article: " + response.title;
  });
  // chrome.tabs.sendMessage(tab.id, {message: "getMinutes"}, function(response) {
  //   document.getElementById('readingTime').innerHTML = "Estimated Reading Time: " + response.minutes + " minutes";
  // });
});

let toggle = document.getElementById('switch');

function getValue(callback) {
	chrome.storage.sync.get('checked', callback);
};

getValue(function(key){ // sets checkbox checked state according to the state saved in chrome.storage.sync
	document.getElementById('switch').checked = key['checked'];
	console.log("Checkbox state set to " + key['checked']);
});

toggle.addEventListener('change', (event) => {
	let message_bool = event.target.checked
	chrome.storage.sync.set({'checked': message_bool}, function(){ // checkbox state in chrome.storage.sync is changed
		console.log("Checkbox state changed to " + message_bool);
	});
	chrome.tabs.query({active: true,currentWindow:true},function(tabs){
		chrome.tabs.sendMessage(tabs[0].id, {message: message_bool}); // sends message to content.js to change link colours
	});
});

// change file upload button when there is a file already in storage
// save file in chrome.storage.local 