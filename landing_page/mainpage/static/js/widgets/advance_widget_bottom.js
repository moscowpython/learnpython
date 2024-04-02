document.addEventListener("DOMContentLoaded", function() {
    var script = document.getElementById('f5be3bcced9b8d99a4cc095aadcc152acc1c0aa0');

	var par = script.parentNode;
	script.parentNode.style.overflow = 'hidden';

	var iframe = document.createElement('iframe');
	iframe.src = 'https://learnpythonru.getcourse.ru/pl/lite/widget/widget'
		+ "?" + window.location.search.substring(1)
		+ "&id=1151238"
		+ "&ref=" + encodeURIComponent(document.referrer)
		+ "&loc=" + encodeURIComponent(document.location.href);
	iframe.style.width = '100%';
	iframe.style.height = '0px';
	iframe.style.border = 'none';
	iframe.style.overflow = 'hidden';
	iframe.setAttribute('allowfullscreen', 'allowfullscreen');
    iframe.className = '51';
	iframe.id = 'c6b45c08ef83f13b64a41560165b2147de61cf2a' + '_' + iframe.className;
	// name можно получить изнутри iframe
	iframe.name = iframe.className;

	var iframeId = iframe.id;

	var gcEmbedOnMessage = function(e) {
		var insertedIframe = document.getElementById(iframeId);
		if (!insertedIframe) {
			return;
		}

		if (e.data.uniqName == 'f5be3bcced9b8d99a4cc095aadcc152acc1c0aa0') {
			if (e.data.height) {
			    if (e.data.iframeName) {
					if (e.data.iframeName == iframe.name) {
                        par.style.height = ( e.data.height ) + "px";
						insertedIframe.style.height = (e.data.height) + "px";
                    }
                } else {
                    par.style.height = ( e.data.height ) + "px";
					insertedIframe.style.height = (e.data.height) + "px";
                }
            }
		}
	};

	if (window.addEventListener) {
		window.addEventListener("message", gcEmbedOnMessage, false);
	}  else if (window.attachEvent) {
		window.attachEvent('onmessage', gcEmbedOnMessage)
	} else {
		window['onmessage'] = gcEmbedOnMessage
	}

	script.parentNode.insertBefore(iframe, script);
	par.removeChild( script )
});

var getLocation = function(href) {
	var l = document.createElement("a");
	l.href = href;
	return l;
};

var currentScript = document.currentScript || (function() {
	var scripts = document.getElementsByTagName('script');
	return scripts[scripts.length - 1];
})();

var domain = ( (getLocation( currentScript.src )).hostname );