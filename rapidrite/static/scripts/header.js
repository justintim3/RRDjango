document.write(
		'<div id="logo"><img src="images/logo.png"></div>' +
    	'<div id="acc_info">' +
    		'<a href="signup.html" id="signup">Sign Up</a>' +
    		'<a href="login.html" id="login">Log In</a>' +
    	'</div>' +
		'<nav>' +   		
			'<a href="homepage.html">Home</a>' +
    		'<a href="#news.html">News</a>' +
    		'<a href="comic.html">Comics</a>' +
			'<a href="#account.html">Account</a>' +    	
			'<a href="#about.html">About</a>' +
    	'</nav>'
    	);

var pathName = window.location.pathname;
console.log(pathName)
