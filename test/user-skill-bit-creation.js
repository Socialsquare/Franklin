var assert = require("assert"),
	test = require('selenium-webdriver/testing'),
	webdriver = require('selenium-webdriver'),
	driver;

test.before(function() {
	driver = new webdriver.Builder().
		usingServer("http://localhost:9515/").
		withCapabilities(webdriver.Capabilities.chrome()).
		build();
	driver.manage().window().maximize() 
});

function randomString() {
	var randomness = Math.round(Math.random() * (99999-10000) + 10000); // [10000;99999]
	return new String(randomness);
}

var admin_username = "admin";
var admin_password = "never-use-this-in-production";
var training_bit_imagepath = "/home/kraen/Billeder/bibtekkonf.jpg";

test.after(function() {
	driver.quit();
});

var randomness = randomString();
var regular_username = "john-doe"+randomness;
var regular_password = randomness +":"+ randomness;

function signOut() {
	// Sign out
	driver.findElement(webdriver.By.id('logged-in-menu')).click();
	driver.findElement(webdriver.By.linkText('Sign out')).click();
}

function closeModal() {
	if(driver.findElements(webdriver.By.className('reveal-modal-bg')).length > 0) {
		driver.findElement(webdriver.By.className('reveal-modal-bg')).click();
	}
}

test.describe('Signing up a user', function() {

	test.it('Navigating to the frontpage should show the frontpage.', function() {
		driver.get("http://127.0.0.1:8000/");

		driver.getTitle().then(function(title) {
			assert.equal("Global Change Lab", title);
		});

		var announcement = driver.findElement(webdriver.By.className('announcement'));
		announcement.getText().then(function(text) {
			assert.notEqual(text.indexOf("CHANGE"), -1);
			assert.notEqual(text.indexOf("BIT BY BIT"), -1);
		});
	
	});

	test.it('Clicking the sign up on the frontpage should take one to the signup page.', function() {
	
		var signUpButton = driver.findElement(webdriver.By.linkText('SIGN UP'));

		signUpButton.click();

		var header = driver.findElement(webdriver.By.className('column-header'));

		header.getText().then(function(title) {
			assert.equal("Sign up for a Global Change Lab account", title);
		});

		driver.findElement(webdriver.By.name('email')).sendKeys("kh+"+randomness+"@bitblueprint.com");
		driver.findElement(webdriver.By.name('username')).sendKeys(regular_username);
		driver.findElement(webdriver.By.name('password1')).sendKeys(regular_password);
		driver.findElement(webdriver.By.name('password2')).sendKeys(regular_password);
		driver.findElement(webdriver.By.name('terms')).click();

		driver.findElement(webdriver.By.css('button[type=submit]')).click();

		// When the user has been created it is greeted.
		driver.findElement(webdriver.By.id('new-user-greeter')).getText().then(function(text) {
			assert.notEqual(text.indexOf(regular_username), -1);
		});

		signOut();

	});
});

var skill_name = "Test Skill "+randomString();
var training_bit_names = [];

test.describe('A superuser can login and create shareable content.', function() {

	test.it('A superuser can login.', function() {
		// Go to the login page.
		driver.findElement(webdriver.By.id('logged-in-menu')).click();
		driver.findElement(webdriver.By.name('login')).sendKeys(admin_username);
		driver.findElement(webdriver.By.name('password')).sendKeys(admin_password);
		driver.findElement(webdriver.By.css('button[type=submit]')).click();
	});

	test.it('A superuser can create a skill.', function() {
		// Go to the login page.
		driver.findElement(webdriver.By.linkText('TRAINER DASHBOARD')).click();
		driver.findElement(webdriver.By.linkText('ADD NEW SKILL')).click();

		driver.findElement(webdriver.By.name('name')).sendKeys(skill_name);
		driver.findElement(webdriver.By.name('description')).sendKeys("The description of the "+skill_name);
		driver.findElement(webdriver.By.css('input[type=radio][name=is_draft][value=False]')).click();
		driver.findElement(webdriver.By.css('button[type=submit]')).click();
	});

	test.it('A superuser can create a couple of training bits.', function() {
		// Create three random training bits.
		for(var i = 0; i < 3; i++) {
			driver.findElement(webdriver.By.linkText('TRAINER DASHBOARD')).click();
			driver.findElement(webdriver.By.linkText('ADD NEW TRAINING BIT')).click();
			var randomness = randomString();
			var name = "Test training bit "+randomness;
			training_bit_names.push(name);
			driver.findElement(webdriver.By.name('name')).sendKeys(name);
			driver.findElement(webdriver.By.name('image')).sendKeys(training_bit_imagepath);
			driver.findElement(webdriver.By.name('description')).sendKeys("The description of the Test training bit "+randomness);
			driver.findElement(webdriver.By.css('input[type=radio][name=is_draft][value=False]')).click();
			driver.findElement(webdriver.By.css('button[type=submit]')).click();
		}
	});

	test.it('A superuser can link the training bits to the skill.', function() {
		driver.findElement(webdriver.By.linkText('TRAINER DASHBOARD')).click();

		// Locate the skill.
		driver.findElement(webdriver.By.linkText(skill_name)).click();

		// Locate the element on which to drop the training bits.
		var chosenList = driver.findElement(webdriver.By.id("trainingbits-chosen-list"));
		// Create three random training bits.
		for(var n in training_bit_names) {
			var name = training_bit_names[n];
			var bitElement = driver.findElement(webdriver.By.xpath("//span[text()='" +name+ "']"));
			
			new webdriver.ActionSequence(driver).
				dragAndDrop(bitElement, chosenList).
				perform();
		}
		driver.findElement(webdriver.By.css('button[type=submit]')).click();
	});

	test.it('An admin can sign out.', function() {
		signOut();
	});

});

test.describe('A regular user I can login and share content.', function() {

	test.it('A regular user can login.', function() {
		// Go to the login page.
		driver.findElement(webdriver.By.id('logged-in-menu')).click();
		driver.findElement(webdriver.By.name('login')).sendKeys(regular_username);
		driver.findElement(webdriver.By.name('password')).sendKeys(regular_password);
		driver.findElement(webdriver.By.css('button[type=submit]')).click();
	});

	test.it('A regular user can locate a skill created by the admin.', function() {
		// Go to the login page.
		driver.findElement(webdriver.By.linkText('SKILLS')).click().then(function() {
		    driver.sleep(1000);
		});
		// Close a box with animation.
		if(driver.findElement(webdriver.By.className('close')).isDisplayed()) {
			driver.findElement(webdriver.By.className('close')).click().then(function() {
			    driver.sleep(1000);
			});
		}

		driver.findElement(webdriver.By.linkText(skill_name.toUpperCase())).click().then(function() {
		    driver.sleep(1000);
		});
	});

	/*
	test.it('A regular user can start a skill.', function() {
		driver.findElement(webdriver.By.linkText('START THIS SKILL')).click();
		// Close the modal if it appears.
		closeModal();
	});
	*/

	test.it('A regular user can start a training bit.', function() {
		var training_bit_name = training_bit_names[0];
		//driver.findElement(webdriver.By.linkText(training_bit_name)).click();
		var bits = driver.findElements(webdriver.By.className(".trainingbit-name"));
		// Click the first.
		bits[0].click();

		driver.findElement(webdriver.By.linkText("START THIS TRAINING BIT")).click();

		driver.findElement(webdriver.By.name("name")).sendKeys("This is awesome!");
		driver.findElement(webdriver.By.name("name")).sendKeys("This is an awesome description - " + randomString());
		driver.findElement(webdriver.By.className("share-button")).click();
	});

	/*
	test.it('A regular user can start a training bit.', function() {
		for(var n in training_bit_names) {
			var bit_name = training_bit_names[n];
			driver.findElement(webdriver.By.linkText(bit_name)).click();
		}
	});
	*/
});


test.describe('The "Shares" page shouldn´t have elements stacking ontop of each other.', function() {

	test.it('Should be the case that all elements on the page clears each other.', function() {
	
		driver.get("http://127.0.0.1:8000/");
		var signUpButton = driver.findElement(webdriver.By.linkText('TRAINER DASHBOARD'));
		/*
		var searchBox = driver.findElement(webdriver.By.name('q'));
		searchBox.sendKeys('webdriver');
		searchBox.getAttribute('value').then(function(value) {
			assert.equal(value, 'webdriver');
		});
		*/
	});
});
