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

function signOut() {
	// Sign out
	driver.findElement(webdriver.By.id('logged-in-menu')).click();
	driver.findElement(webdriver.By.linkText('Sign out')).click();
}

function signIn( username, password ) {
	// Go to the login page.
	driver.get("http://localhost:8000/user/login/");
	driver.findElement(webdriver.By.name('login')).sendKeys(username);
	driver.findElement(webdriver.By.name('password')).sendKeys(password);
	driver.findElement(webdriver.By.css('button[type=submit]')).click();
}

function receiveMockedMail( mail_callback ) {
	fs.readdir(MAIL_DIRECTORY, function(err, files) {
		// Finding the newest mail.
		for(f in files) {
			var file = files[f];
			var file_path = MAIL_DIRECTORY +"/"+ file;
			var file_stat = fs.statSync(file_path);
			var newest_file;
			var newest_file_ctime;
			if(!newest_file || newest_file.ctime < file_stat.ctime) {
				newest_file = f;
				newest_file_ctime = file_stat.ctime;
			}
		}
		// Finding the first link in the newest mail.
		var mail_file_path = MAIL_DIRECTORY +"/"+ files[f];
		var mail_content = fs.readFileSync( mail_file_path, { encoding: 'utf8' } );
		mail_callback( mail_content );
	});
}

test.before(function() {
	driver = new webdriver.Builder().
		usingServer("http://localhost:9515/").
		withCapabilities(webdriver.Capabilities.chrome()).
		build();
	driver.manage().window().maximize();
	// signIn();
});

test.after(function() {
	driver.quit();
});

// Check that no two shares overlap on the /shares page.
test.describe('The activation workflow', function() {

	var regular_user;

	test.it('can sign up users', function() {
		var email = REGULAR_USERNAME_PREFIX + "-" + randomString() + "@bitblueprint.com";
		var username = REGULAR_USERNAME_PREFIX + "-" + randomString();
		var password = REGULAR_PASSWORD;
		driver.get("http://localhost:8000/user/signup/");
		driver.findElement(webdriver.By.name('email')).sendKeys(email);
		driver.findElement(webdriver.By.name('username')).sendKeys(username);
		driver.findElement(webdriver.By.name('password1')).sendKeys(password);
		driver.findElement(webdriver.By.name('password2')).sendKeys(password);
		driver.findElement(webdriver.By.name('terms')).click();
		driver.findElement(webdriver.By.css('button[type=submit]')).click();
		regular_user = {
			email: email,
			username: username,
			password: password
		};
	});

	test.it('sends a link and the account can be activated', function() {
		receiveMockedMail(function(activation_mail) {
			var link_regexp = 'http://localhost:8000/user/confirm-email/([^/]*)/';
			var link = activation_mail.match(/http:\/\/localhost:8000\/user\/confirm-email\/([^\/]*)\//g);
			assert.equal(link.length > 0, true, "The link contains an activation link.");
			link = link[0];
			driver.get(link);

			driver.findElement(webdriver.By.tagName('h1')).getText().then(function(text) {
				assert( text === 'CONFIRM E-MAIL ADDRESS', "the welcome message exists." );
			});
			// assert.true(webdriver.getPageSource().contains("Confirm E-mail Address"), "The page contains the right title");
			driver.findElement(webdriver.By.css('button[type=submit]')).click();
		});
	});

	test.it('redirects to the welcome page when submitting the activation', function() {
		// Page contains the welcome message.
		driver.findElement(webdriver.By.css('h1.white')).getText().then(function(text) {
			assert( text === 'Hi '+regular_user.username+',', "the welcome message exists." );
		});
		driver.findElement(webdriver.By.css('h1.red')).getText().then(function(text) {
			assert( text === 'Welcome to Global Change Lab!', "the welcome message exists." );
		});
	})

	test.it('redirects to the normal page when logging in a second time', function() {
		driver.sleep(5000);
		signOut();
		signIn( regular_user.username, regular_user.password );
		// Page contains the welcome message.
		driver.findElement(webdriver.By.css('#profile-bar h1')).getText().then(function(text) {
			assert( text === regular_user.username.toUpperCase() );
		});
		driver.findElement(webdriver.By.css('h2.section-title')).getText().then(function(text) {
			assert( text === "COMPLETED SKILLS" );
		});
	})
});