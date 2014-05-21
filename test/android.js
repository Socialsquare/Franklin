// Reproducing "Med aktivering af email ved sign up er welcome flowet væk"
// See: https://podio.com/socialsquare/global-change-lab/apps/issues/items/121

var assert = require("assert"),
	test = require('selenium-webdriver/testing'),
	webdriver = require('selenium-webdriver'),
	fs = require('fs');

var driver;

function randomString() {
	var randomness = Math.round(Math.random() * (99999-10000) + 10000); // [10000;99999]
	return new String(randomness);
}

var REGULAR_USERNAME_PREFIX = "regular";
var REGULAR_PASSWORD = "never-use-this-in-production";
var MAIL_DIRECTORY = "/tmp/gcl-messages";
var BASE_URL = "http://kh.vpn.bitblueprint.com:8000/";

function signOut() {
	// Sign out
	driver.findElement(webdriver.By.id('logged-in-menu')).click();
	driver.findElement(webdriver.By.linkText('Sign out')).click();
}

function signIn( username, password ) {
	// Go to the login page.
	// driver.get(BASE_URL + "user/login/");
	// Navigate to the sign in page.
	driver.get(BASE_URL);
	driver.findElement(webdriver.By.css(".menu-icon")).click();
	driver.findElement(webdriver.By.css("#logged-in-menu")).click();

	driver.findElement(webdriver.By.name('login')).sendKeys(username);
	driver.findElement(webdriver.By.name('password')).sendKeys(password);
	driver.findElement(webdriver.By.css('button[type=submit]')).click();
}

test.before(function() {
	//var capabilities = webdriver.Capabilities.android();
	var capabilities = {
		'chromeOptions': {
			'androidPackage': 'com.android.chrome',
		}
	};
	driver = new webdriver.Builder().
		usingServer("http://localhost:9515/").
		withCapabilities(capabilities).
		build();
	// driver.manage().window().maximize();
	// signIn();
});

test.after(function() {
	driver.quit();
});

// Check that no two shares overlap on the /shares page.
test.describe('The activation workflow', function() {

	test.it('can sign up users', function() {
		signIn(REGULAR_USERNAME_PREFIX, REGULAR_PASSWORD);
		
		driver.sleep(1000000);
	});

});