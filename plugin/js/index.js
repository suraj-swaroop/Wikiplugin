chrome.tabs.getSelected(null, function(tab) {
  // Send a request to the content script.
  chrome.tabs.sendMessage(tab.id, {message: "getInfo"}, function(response) {
    document.getElementById('articleName').innerHTML = "Wikipedia Article: " + response.title;
    wiki_title = response.title;
  });
});

toggle.addEventListener('change', (event) => {
  beautifier.setValue("SELECT `To`, `Count`\n  FROM `Clickstream`\n  WHERE `From`='" + wiki_title + "';");
  config.sql.exec("clickstream");
});

function hideToggle(){
  document.getElementById('recolourToggle').style.visibility = "hidden";
}

function showToggle(){
  document.getElementById('recolourToggle').style.visibility = "visible";
}

hideToggle();

// function getDBFileValue(callback) {
//   chrome.storage.local.get('dbfile', callback);
// };

var background = (function () {
  var r = {};
  chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.path === 'background-to-ui') {
      for (var id in r) {
        if (request.method === id) r[id](request.data);
      }
    }
  });
  /*  */
  return {
    "receive": function (id, callback) {r[id] = callback},
    "send": function (id, data) {chrome.runtime.sendMessage({"path": 'ui-to-background', "method": id, "data": data})}
  }
})();

var config = {
  "time": {
    "start": null,
    "tic": function () {
      config.loader.start();
      config.time.start = performance.now();
    },
    "toc": function (e, r) {
      config.loader.stop();
      var total = Math.round(((performance.now() - config.time.start) / 1000) * 100) / 100 || "0.00";
    	if (e) config.sql.info.textContent = config.sql.info.textContent + ' ' + e + (r ? ": " + total + "sec" : '');
    }
  },
  "loader": {
    "stop": function () {
      var loader = document.getElementById("loader");
      var img = loader.querySelector("img");
      img.style.display = "none";
    },
    "start": function () {
      var loader = document.getElementById("loader");
      var img = loader.querySelector("img");
      img.style.display = "initial";
    }
  },
  "app": {
    "worker": new Worker("vendor/sql/worker.sql.js"),
    "error": function (e) {config.time.toc(e.message, false)},
    "clear": function () {
      config.time.tic();
      config.sql.info.textContent = '';
      // config.sql.output.textContent = '';
      config.time.toc('', false);
    },
    "savedb": function () {
      console.log('savedb');
    	config.app.worker.onmessage = function (e) {
        config.time.toc(chrome.i18n.getMessage('app_notify6'), true);
    		var arraybuffer = e.data.buffer;
    		var blob = new Blob([arraybuffer]);
    		var a = document.createElement('a');
        a.download = "sql.db";
    		a.href = window.URL.createObjectURL(blob);
        document.body.appendChild(a);
    		a.onclick = function () {
          window.setTimeout(function () {
            window.URL.revokeObjectURL(a.href);
            a.parentNode.removeChild(a);
          }, 1500)
        };
    		a.click();
    	};
      /*  */
    	config.time.tic();
    	config.app.worker.postMessage({"action": "export"});
    },
    "execute": function (cmd, type) {
      console.log(cmd);
    	config.time.tic();
    	config.app.worker.onmessage = function (e) {
    		var results = e.data.results;
        console.log(results);
        if (results) {
          if(type=="minutes"){
            if(results.length == 0){
              document.getElementById('readingTime').innerHTML = "Estimated Reading Time Unavailable";
            } else {
              document.getElementById('readingTime').innerHTML = "Estimated Reading Time: " + Math.ceil((results[0].values)[0][0]) + " minutes";
            }
            showToggle();
          }
          if(type=="clickstream"){
            //need to send to content.js
            chrome.tabs.query({active: true,currentWindow:true},function(tabs){
              chrome.tabs.sendMessage(tabs[0].id, {message: results[0].values}); // sends message to content.js to change link colours
            });
          }
      		config.time.toc(chrome.i18n.getMessage('app_notify4'), true);
      		config.time.tic();
      		// config.sql.output.textContent = '';
      		// for (var i = 0; i < results.length; i++) {
        //     config.sql.output.appendChild(config.create.table(results[i].columns, results[i].values));
        //   }
      		config.time.toc(chrome.i18n.getMessage('app_notify5'), true);
        }
    	}
      /*  */
      config.app.worker.postMessage({"action": 'exec', "sql": cmd});
      // config.sql.info.textContent = `${chrome.i18n.getMessage('app_notify3')}... >>`;
    }
  },
  "sql": {
    "file": null,
    "info": document.getElementById("info"),
    // "save": document.getElementById("save"),
    // "run": document.getElementById("execute"),
    "dbfile": document.getElementById("dbfile"),
    // "output": document.getElementById("output"),
    "commands": document.getElementById("commands"),
    "exec": function (type="") {config.app.execute(beautifier.getValue() + ';', type)},
    "size": function (s) {
      if (s) {
        if (s >= Math.pow(2, 30)) {return (s / Math.pow(2, 30)).toFixed(1) + "GB"};
        if (s >= Math.pow(2, 20)) {return (s / Math.pow(2, 20)).toFixed(1) + "MB"};
        if (s >= Math.pow(2, 10)) {return (s / Math.pow(2, 10)).toFixed(1) + "KB"};
        return s + "B";
      } else return '';
    },
  },
  "create": {
    "table": function () {
      var add = function (a, b, c) {
        if (a) {
          var parent = document.createElement(c);
          for (var i = 0; i < a.length; i++) {
            var tmp = document.createElement(b);
            tmp.textContent = a[i];
            parent.appendChild(tmp);
          }
          return parent;
        }
        /*  */
        var parent = document.createElement(c);
        var tmp = document.createElement(b);
        tmp.textContent = "null";
        parent.appendChild(tmp);
        return parent;
      };
      /*  */
      return function (columns, values) {
        var table  = document.createElement("table");
        table.appendChild(add(columns, "th", "thead"));
        for (var i = 0; i < values.length; i++) table.appendChild(add(values[i], "td", "tr"));
        return table;
      }
    }()
  }
};

var beautifier = CodeMirror.fromTextArea(config.sql.commands, {
  "autofocus": true,
  "smartIndent": true,
  "lineNumbers": true,
  "matchBrackets": true,
  "mode": 'text/x-mysql',
  "indentWithTabs": true,
  "viewportMargin": Infinity
});

function loadDBFile(reader){
  var fileinfo = document.getElementById("fileinfo");
  console.log("file");
  console.log(config.sql.file.name);
  fileinfo.textContent = config.sql.file.name + ' ' + config.sql.size(config.sql.file.size);
  /*  */
  reader.onload = function () {
    config.app.worker.onmessage = function () {
      config.time.toc(chrome.i18n.getMessage('app_notify1'), true);
      // beautifier.setValue("SELECT `name`, `sql`\n  FROM `sqlite_master`\n  WHERE type='table';");
      beautifier.setValue("SELECT `AdjustedReadingTimeMinutes`\n  FROM `Difficulty`\n  WHERE Article='" + wiki_title + "';");
      config.sql.exec("minutes");
    };
    /*  */
    config.time.tic();
    try {config.app.worker.postMessage({"action": 'open', "buffer": reader.result}, [reader.result])}
    catch (e) {config.app.worker.postMessage({"action": 'open', "buffer": reader.result})}
  }
  /*  */
  if (config.sql.file) reader.readAsArrayBuffer(config.sql.file);
};

var load = function () {
  // document.querySelector('.teaser').href = `https://chrome.google.com/webstore/detail/${chrome.runtime.id}/reviews`;
  
  var localization = new Localize();
  localization.init();
  localization.localizeHtmlPage();

  config.time.tic();
  config.app.worker.onerror = config.app.error;
  window.removeEventListener("load", load, false);
  config.app.worker.postMessage({"action": "open"});
  // config.sql.run.addEventListener("click", config.sql.exec, true);
  // config.sql.save.addEventListener("click", config.app.savedb, true);
  /*  */
  chrome.storage.local.get('dbfile', function(result){
    console.log('what');
    if(result.dbfile != null){
      var reader = new FileReader();
      config.sql.file = result.dbfile;
      console.log('GET');
      console.log(config.sql.file);
      console.log(typeof config.sql.file);
      loadDBFile(reader);
      
    }
  })
  config.sql.dbfile.addEventListener("change", function () {
    var reader = new FileReader();
  	config.sql.file = config.sql.dbfile.files[0];
    console.log(JSON.stringify(config.sql.file));
    console.log('SET');
    console.log(config.sql.file);
    console.log(typeof config.sql.file);
    //chrome.storage.local.set({'dbfile': config.sql.file});
    loadDBFile(reader);
  });
  /*  */
  // var clear = document.getElementById("clear");
  // var reload = document.getElementById("reload");
  // var sample = document.getElementById("sample");
  var commands = document.getElementById("commands");
  /*  */
  // clear.addEventListener("click", function () {config.app.clear()});
  // reload.addEventListener("click", function () {document.location.reload()});
  
  /*  */
 //  sample.addEventListener("click", function () {
 //    beautifier.setValue(` DROP TABLE IF EXISTS colleagues;
 // CREATE TABLE colleagues(id integer, name text, title text, manager integer, hired date, salary integer, commission float, dept integer);
 //  INSERT INTO colleagues VALUES (1,'JOHNSON','ADMIN',6,'2011-12-17',18000,NULL,4);
 //  INSERT INTO colleagues VALUES (2,'HARDING','MANAGER',9,'2011-02-02',52000,300,3);
 //  INSERT INTO colleagues VALUES (3,'TAFT','SALES I',2,'2015-01-02',25000,500,3);
 //  INSERT INTO colleagues VALUES (4,'HOOVER','SALES II',2,'2011-04-02',27000,NULL,3);
 //  INSERT INTO colleagues VALUES (5,'LINCOLN','TECH',6,'2012-06-23',22500,1400,4);
 //  INSERT INTO colleagues VALUES (6,'GARFIELD','MANAGER',9,'2013-05-01',54000,NULL,4);
 //  INSERT INTO colleagues VALUES (7,'POLK','TECH',6,'2014-09-22',25000,NULL,4);
 //  INSERT INTO colleagues VALUES (8,'GRANT','ENGINEER',10,'2014-03-30',32000,NULL,2);
 //  INSERT INTO colleagues VALUES (9,'JACKSON','CEO',NULL,'2011-01-01',75000,NULL,4);
 //  INSERT INTO colleagues VALUES (10,'FILLMORE','MANAGER',9,'2012-08-09',56000,NULL,2);
 //  INSERT INTO colleagues VALUES (11,'ADAMS','ENGINEER',10,'2015-03-15',34000,NULL,2);
 //  INSERT INTO colleagues VALUES (12,'WASHINGTON','ADMIN',6,'2011-04-16',18000,NULL,4);
 //  INSERT INTO colleagues VALUES (13,'MONROE','ENGINEER',10,'2017-12-03',30000,NULL,2);
 //  INSERT INTO colleagues VALUES (14,'ROOSEVELT','CPA',9,'2016-10-12',35000,NULL,1);

 // SELECT name, hired FROM colleagues ORDER BY hired ASC;
 // SELECT title, COUNT(*) AS count, (AVG(salary)) AS salary FROM colleagues GROUP BY title ORDER BY salary DESC;`);
 //  });

  config.time.toc(chrome.i18n.getMessage('app_notify2'), false);
};

window.addEventListener("load", load, false);


