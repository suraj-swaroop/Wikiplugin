var curr_url = window.location.href;
// chrome.runtime.onMessage.addListener(recolour);
s_arr = []

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
 if (request.message == "getInfo"){
   sendResponse({title: document.getElementById("firstHeading").textContent});
 } else if (typeof request.message === "boolean"){
   recolour(request.message);
 } else if (typeof request.message === "object"){
   s_arr = request.message;
   recolour(true);
 }
 else
   sendResponse({}); // Send nothing..
});

// function from https://stackoverflow.com/questions/48719873/how-to-get-median-and-quartiles-percentiles-of-an-array-in-javascript-or-php
function Quartile(data, q) {
  var pos = ((data.length) - 1) * q;
  var base = Math.floor(pos);
  var rest = pos - base;
  if( (data[base+1]!==undefined) ) {
    return data[base] + rest * (data[base+1] - data[base]);
  } else {
    return data[base];
  }
}

function getValue(callback) {
	chrome.storage.sync.get('checked', callback);
};

// The following function is run everytime the page is (re)loaded. Colours links according to the checked state in chrome.storage.sync
getValue(function(key){
	if (key['checked']) {
		recolour(true);
	};
});

function recolour(message) {
	let links = document.getElementById("bodyContent").getElementsByTagName("a");
	let red_hex = ['#FF9999', '#FF0000', '#990000', '#660000']; // 4 red colours of different values
  console.log(s_arr);
  var counts = s_arr.map(function(value,index) { return value[1]; }).sort();
  q_25 = Quartile(counts, 0.25);
  q_50 = Quartile(counts, 0.5);
  q_75 = Quartile(counts, 0.75);
	for (link of links) {
        if (link.style.color != '#0b0080'){ // keep clicked links dark blue but recolor red links to blue
            link.style.color = '#0645ad';
        }
		if ((link.href && link.href.startsWith("https://en.wikipedia.org/wiki/")) && (link.href.indexOf('#cite_note') == -1)) {
            if (message){
                var name = link.href.match(/wiki\/(.*)/)[1];
                temp = s_arr.filter(function(el){return el[0].indexOf(name) !== -1;})[0];
                if (!temp) {
                    continue;
                }
                if (temp[1] <= q_25){
                    link.style.color = red_hex[0];
                    continue;
                } else if (temp[1] <= q_50){
                    link.style.color = red_hex[1];
                    continue;
                } else if (temp[1] <= q_75){
                    link.style.color = red_hex[2];
                    continue;
                } else {
                    link.style.color = red_hex[3];
                }
            } else { // changes links back to blue if toggle is clicked again
                link.style.color = '#0645ad'; 
            }
		}
	}
};
// path: C:\Users\User\AppData\Local\Google\Chrome\User Data
