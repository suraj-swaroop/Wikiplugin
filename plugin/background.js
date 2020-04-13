  chrome.runtime.onInstalled.addListener(function() {
  	chrome.storage.sync.set({checked: false}, function() {
  		console.log("Checkbox checked state is automatically false"); // checkbox is false when first loaded
  	})
    chrome.storage.local.set({dbfile: null});
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {hostEquals: 'en.wikipedia.org'},
        })
        ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
  });
  	
