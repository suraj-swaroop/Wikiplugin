console.log("Someone clicked the toggle!");
chrome.runtime.onMessage.addListener(recolour);

function getValue(callback) {
	chrome.storage.sync.get('checked', callback);
};

// The following function is run everytime the page is (re)loaded. Colours links according to the checked state in chrome.storage.sync
getValue(function(key){
	if (key['checked']) {
		recolour(true, null, null);
	};
});

function recolour(message, sender, sendresponse) {
	let links = document.getElementById("bodyContent").getElementsByTagName("a");
	let red_hex = ['#FF6666', '#FF0000', '#990000', '#4C0000']; // 4 red colours of different values
	for (link of links) {
		if (link.href && link.href.startsWith("https://en.wikipedia.org/wiki/")) {
			if (message) {
				link.style.color = red_hex[Math.floor(Math.random() * red_hex.length)]; // randomly changes link colours to one of the reds for now
			} else {
				link.style.color = '#0645AD'; // changes links back to blue
			}
		}
	}
};