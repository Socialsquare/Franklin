var webdriver = require('selenium-webdriver');

var admin_username = "admin";
var admin_password = "never-use-this-in-production";
var regular_username = "regular";
var regular_password = "never-use-this-in-production";

exports.before = function() {
	// TODO: Consider how one maximizes the window.
	browser.clickText = function(text, css_selector, callback) {
		if(!css_selector) {
			css_selector = "a";
		}
		var selector = "//" +css_selector+ "[contains(.,'" +text+ "')]";
		if(callback) {
			return this.click(selector, callback);
		} else {
			return this.click(selector);
		}
	};
	browser.isVisibleText = function(text, css_selector, callback) {
		if(!css_selector) {
			css_selector = "a";
		}
		var selector = "//" +css_selector+ "[contains(.,'" +text+ "')]";
		return this.isVisible(selector, callback);
	};
}

exports.after = function() {
	// TODO: Consider closing the windows
}

exports.random_string = function() {
	var randomness = Math.round(Math.random() * (99999-10000) + 10000); // [10000;99999]
	return new String(randomness);
}

exports.login = function(username, password, callback) {
	return browser
		.url("http://localhost:8000/user/login/")
		.setValue('input[name=login]', username)
		.setValue('input[name=password]', password)
		.click('button[type=submit]')
		.waitFor('#logged-in-menu', 1000, callback);
}

exports.login_admin = function( callback ) {
	return exports
		.login(admin_username, admin_password, callback)
		.waitFor('#admin-dashboard-button', 1000);
}

exports.login_regular = function( callback ) {
	return exports.login(regular_username, regular_password, callback);
}

exports.appUrl = function(url) {
	return browser
		.url("http://localhost:8000/" + url);
}