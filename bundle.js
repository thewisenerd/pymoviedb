var callback, container, params, repo, url, username, client_id, client_secret, access_token;
username = "thewisenerd";
repo = "movie_db";

var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/\r\n/g,"\n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}

function write_elem(content, count){
	/*
	* content[0] : title
	* content[1] : imdbid
	* content[2] : year
	* content[3] : quality
	* //TODO: mov[4] : enc. notes(?)
	*/

	container = $("#movielist"); //helper

	var writeback = '';

	writeback += "<button onclick=\"javascript:dialoggen('" + content[1] + "', '" + count + "')\" " + 'class="btn btn-flat btn-default" data-toggle="modal" data-target="#complete-dialog' + count + '"><span class="badge">' + count + '</span> ' + content[0] + '<div class="ripple-wrapper"></div></button>' + "\n";
	writeback += "	<div id=\"complete-dialog" + count + "\" " + 'class="modal fade" tabindex="-1" style="display: none;" aria-hidden="true">' + "\n";
	writeback += '		<div class="modal-dialog">' + "\n";
	writeback += '			<div class="modal-content">' + "\n";
	writeback += '				<div class="modal-header">' + "\n";
	writeback += '					<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&#215;</button>' + "\n";
	writeback += '					<div class="row vertical-align">' + "\n";
	writeback += "					<div id=\"dialog-img-" + count + "\" " + 'class="movie-poster col-xs-12 col-md-4">' + "\n";
	writeback += '						<div class="spinner2"><div class="dot1"></div><div class="dot2"></div></div>' + "\n";
	writeback += '					</div>' + "\n";
	writeback += '					<div class="col-xs-12 col-md-8" align="left">' + "\n";
	writeback += '						<h3 class="modal-title">' + content[0] + '</h3>' + "\n";
	writeback += '					</div>' + "\n";
	writeback += '				</div>' + "\n";
	writeback += '			</div>' + "\n";
	writeback += '			<div class="modal-body">' + "\n";
	writeback += '				<div class="list-group">' + "\n";
	writeback += '					<div class="list-group-item">' + "\n";
	writeback += '						<div class="row-action-primary">' + "\n";
	writeback += '							<i class="mdi mdi-calendar"></i>' + "\n";
	writeback += '						</div>' + "\n";
	writeback += '						<div class="row-content">' + "\n";
	writeback += '							<div class="action-secondary"><i class="mdi-material-info"></i></div>' + "\n";
	writeback += '							<h6 class="list-group-item-heading">Year</h6>' + "\n";
	writeback += '							<p class="list-group-item-text">' + content[2] + '</p>' + "\n";
	writeback += '						</div>' + "\n";
	writeback += '					</div>' + "\n";
	writeback += '					<div class="list-group-separator"></div>' + "\n";
	writeback += '					<div class="list-group-item">' + "\n";
	writeback += '						<div class="row-action-primary">' + "\n";
	writeback += '							<i class="mdi-av-video-collection"></i>' + "\n";
	writeback += '						</div>' + "\n";
	writeback += '						<div class="row-content">' + "\n";
	writeback += '							<div class="action-secondary"><i class="mdi-material-info"></i></div>' + "\n";
	writeback += '							<h6 class="list-group-item-heading">Quality</h6>' + "\n";
	writeback += '							<p class="list-group-item-text">' + content[3] + '</p>' + "\n";
	writeback += '						</div>' + "\n";
	writeback += '					</div>' + "\n";
	writeback += '					<div class="list-group-separator"></div>' + "\n";
	writeback += '					<div class="list-group-item">' + "\n";
	writeback += '						<div class="row-action-primary">' + "\n";
	writeback += '							<i class="mdi mdi-movie"></i>' + "\n";
	writeback += '						</div>' + "\n";
	writeback += '						<div class="row-content">' + "\n";
	writeback += '							<div class="action-secondary"><i class="mdi-material-info"></i></div>' + "\n";
	writeback += '							<h6 class="list-group-item-heading">IMDB</h6>' + "\n";
	writeback += '							<p class="list-group-item-text"><a href="http://www.imdb.com/title/' + content[1] + '/" target="_blank">Link<i class="mdi-action-open-in-new"></i></a></p>' + "\n";
	writeback += '						</div>' + "\n";
	writeback += '					</div>' + "\n";
	writeback += '					<div class="list-group-separator"></div>' + "\n";
	writeback += '					<div class="list-group-item">' + "\n";
	writeback += '						<div class="row-action-primary">' + "\n";
	writeback += '							<i class="mdi mdi-tooltip-text"></i>' + "\n";
	writeback += '						</div>' + "\n";
	writeback += '						<div class="row-content">' + "\n";
	writeback += '							<div class="action-secondary"><i class="mdi-material-info"></i></div>' + "\n";
	writeback += '							<h6 class="list-group-item-heading">Summary</h6>' + "\n";
	writeback += '							<p class="list-group-item-text get-summary-btn">' + "\n";
	writeback += '								<div id="dialog-' + count + '">' + "\n";
	writeback += '									<div class="spinner">' + "\n";
	writeback += '										<div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div>' + "\n";
	writeback += '									</div>' + "\n";
	writeback += '								</div>' + "\n";
	writeback += '							</p>' + "\n";
	writeback += '						</div>' + "\n";
	writeback += '					</div>' + "\n";
	writeback += '					<div class="list-group-separator"></div>' + "\n";
	writeback += '				</div>' + "\n";
	writeback += '			</div>' + "\n";
	writeback += '			<div class="modal-footer">' + "\n";
	writeback += '				<!--<a target="_blank" href="http://php.thewisenerd.changeip.org/mailgun-php/?title=' + Base64.encode (content[0]) +  '" class="btn btn-danger btn-fab btn-raised mdi-alert-error" title="report movie"></a>-->' + "\n";
	writeback += '				<button class="btn btn-success" data-dismiss="modal">Close</button>' + "\n";
	writeback += '			</div>' + "\n";
	writeback += '		</div>' + "\n";
	writeback += '	</div>' + "\n";
	writeback += '</div>' + "\n";
	writeback += "\n";

	container.append(writeback);
}

function write_list(content) {
	container = $("#movielist"); //helper
	var arr = content.split("\n");
	for (var i = 0; i < arr.length; i++) {
		var mov = arr[i].split("|");
		if (mov.length < 4) {
			console.log("something wrong with: "+arr[i]);
			continue;
		} else {
			write_elem(mov, i + 1);
		}
	}
}

function dialoggen(imdbid, containerid) {

	var imdb_reflink="http://www.imdb.com/";

	$.ajax({
		type: "GET",
		dataType: "json",
		url: "http://www.omdbapi.com/?i=" + imdbid,
		async:true
	}).done(function(response) {

		if (response.Response == "False") {
			$('#dialog-'+containerid).html("summary not found");
			$('#dialog-'+containerid).show();
			$('#dialog-img-'+containerid).html("<i class=\"mdi-alert-error\"></i>");
		} else {
			$('#dialog-'+containerid).html(response.Plot);
			$('#dialog-'+containerid).show();
			if (response.Poster == "N/A") {
				$('#dialog-img-'+containerid).html("<img src=\"assets/images/poster-not-available.jpg\" width=\"100%\" min-height=\"66px\"></img>");
			} else {
				$('#dialog-img-'+containerid).html("<img src=\"http://php.thewisenerd.changeip.org/spoof_referer/?url=" + Base64.encode(response.Poster) + "&referer=" + Base64.encode(imdb_reflink) + "&content=image&type=jpeg\" width=\"100%\" min-height=\"66px\" onerror=\"this.onerror=null;this.src='assets/images/poster-not-available.jpg';show_err();\" \"></img>");
			}

			$('#dialog-img-'+containerid).show();
		}

		//lemme stop spamming console for now :P
		//console.log(response);

	});


}

$(function() {
	container = $("#movielist"); //helper
	callback = function(response) {
		var content_data = Base64.decode(response.data.content);
		write_list(content_data);
		//console.log(content_data);
	};
	url = "https://api.github.com/repos/" + username + "/" + repo + "/contents/list";
	return $.ajax(url, {
		dataType: "jsonp",
		type: "get"
	}).success(function(response) {
		return callback(response);
	});
});
