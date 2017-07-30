function formatter_text_nbsp_rreplace(str) {
	var output = "";
	var lines = str.split("\n");
	for (x in lines) {
		//count whitespaces from start
		var cnt = 0;
		while (lines[x].charAt(cnt) == " ") { cnt++; }
		//add counted whitespaces as &nbsp; at beginning of line
		for(i=0; i<cnt; i++) { output += "&nbsp;"; }
		//add line without leading whitespaces
		output += lines[x].substring(cnt, lines[x].length);
		//add line break;
		output += "<br />";
	}
	return output;
}

function formatter_text_nbsp_all(str) {
	var x = str;
    while (x.indexOf(" ")  !== -1) { x = x.replace(" ",  "&nbsp;"); }
	while (x.indexOf("\n") !== -1) { x = x.replace("\n", "<br />"); }
	return x;
}

function get_data(id, path) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var elem = document.getElementById(id);
			elem.innerHTML = formatter_text_nbsp_rreplace(this.responseText);
		}
	};
	xhttp.open("GET", path, true);
	xhttp.send();
}

function get_data_nbsp_all(id, path) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var elem = document.getElementById(id);
			elem.innerHTML = formatter_text_nbsp_all(this.responseText);
		}
	};
	xhttp.open("GET", path, true);
	xhttp.send();
}

function accordion(id, path) {
	var elem = document.getElementById(id);
	if (elem.className.indexOf("w3-show") == -1) {
		elem.className += " w3-show";
		get_data(id, path);
	} else {
		elem.className = elem.className.replace(" w3-show", "");
		elem.innerHTML = "... loading ...";
	}
}

function accordion_nbsp_all(id, path) {
	var elem = document.getElementById(id);
	if (elem.className.indexOf("w3-show") == -1) {
		elem.className += " w3-show";
		get_data_nbsp_all(id, path);
	} else {
		elem.className = elem.className.replace(" w3-show", "");
		elem.innerHTML = "... loading ...";
	}
}

function get_time() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById("time").innerHTML = this.responseText;
		}
	};
  xhttp.open("GET", "/api/time", true);
  xhttp.send();
}
get_time();
window.setInterval(get_time, 5000);
