var callback, container, params, repo, url, username, client_id, client_secret, access_token, writeback;
username = "thewisenerd";
repo = "movie_db";
client_id = '033fd886f77377e1d453';
client_secret = 'ed350cb9e77cabcec5f984437fc1401fae871b7c';
access_token = '24ed81fd35e122c39eee0216db1b5a25ba056e10';
container = $('#movielist');


var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/\r\n/g,"\n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}

function write_elem(content, count){
	writeback = '';
	writeback += '<button class="btn btn-flat btn-default" data-toggle="modal" data-target="#complete-dialog' + count + '">' + content[0] + '<div class="ripple-wrapper"></div></button>';
	$('#movielist').append(writeback);//writeback +=
	console.log(writeback);
}

function write_list(content) {
	var arr = content.split("\n");
	for (var i = 0; i < arr.length; i++) {
		var mov = arr[i].split("|");
		if (mov.length < 4) {
			console.log("something wrong with: "+arr[i]);
			continue;
		} else {
			//write_elem(mov, i); not write_elem for now
			//http://www.imdb.com/title/tt0324554/
			$('#movielist').append((i + 1) + ". " + mov[0] + " <a target=\"_blank\" href=\"http://www.imdb.com/title/" + mov[1]+ "/\"> (imdb)</a><br />\n");
			//console.log("movie:" + mov[0] + "|imdb:"+mov[1]);
		}
	}

}

$(function() {
	callback = function(response) {
		var content_data = Base64.decode(response.data.content);
		write_list(content_data);
		//console.log(content_data);
	};
	url = "https://api.github.com/repos/" + username + "/" + repo + "/contents/list?access_token=" + access_token + "&callback=callback&client_id=" + client_id + "&client_secret=" + client_secret;
	return $.ajax(url, {
		dataType: "jsonp",
		type: "get"
	}).success(function(response) {
		return callback(response);
	});
});
