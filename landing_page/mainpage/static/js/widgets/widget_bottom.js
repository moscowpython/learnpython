console.log('in file')

document.addEventListener("DOMContentLoaded", function() {
	var script = document.getElementById('3e6321862d90cf3a72c6198927067b35e82b0b82');
    // var script = document.currentScript;
	var par = script.parentNode;
	script.parentNode.style.overflow = 'hidden';

	var iframe = document.createElement('iframe');
	iframe.src = 'https://learnpythonru.getcourse.ru/pl/lite/widget/widget'
		+ "?" + window.location.search.substring(1)
		+ "&id=1139675"
		+ "&ref=" + encodeURIComponent(document.referrer)
		+ "&loc=" + encodeURIComponent(document.location.href);
	iframe.style.width = '100%';
	iframe.style.height = '0px';
	iframe.style.border = 'none';
	iframe.style.overflow = 'hidden';
	iframe.setAttribute('allowfullscreen', 'allowfullscreen');
    iframe.className = '940';
	iframe.id = 'cc9d55a8a649fc463bf0a580d1c0567f6542b153' + '_' + iframe.className;
	// name можно получить изнутри iframe
	iframe.name = iframe.className;

	var iframeId = iframe.id;

	var gcEmbedOnMessage = function(e) {
		var insertedIframe = document.getElementById(iframeId);
		if (!insertedIframe) {
			return;
		}

		if (e.data.uniqName == '3e6321862d90cf3a72c6198927067b35e82b0b82') {
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