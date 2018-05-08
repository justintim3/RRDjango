document.write(
		'<div id="logo"><img src="static/images/logo.png"></div>' +
    	'<div id="acc_info">' +
    		'<div id="username">' +
    			'<span>Username:</span>' +
    			'<input type="text" name="username" maxlength=20 size=15>' +
    		'</div>' +
    		'<div id="password">' +
    			'<span>Password:</span>' +
    			'<input type="password" name="password" maxlength=20 size=15>' +
    		'</div>' +
    		'<div id="login_button">' +
    			'<button type="submit">Log in</button>' +
    		'</div>' +
    		'<div id="signup_rec">' +
    			"<span>Don't have an account? </span>" +
    			'<a id="signup" href="signup.html">Sign Up</a>' +
    		'</div>' +
    	'</div>' +
		'<nav>' +   		
			'<a href="{% url \'homepage\' %}">Home</a>' +
    		'<a href="#news.html">News</a>' +
    		'<a href="comic.html">Comics</a>' +
			'<a href="profile.html">Account</a>' +    	
			'<a href="#about.html">About</a>' +
    	'</nav>'
    	);


