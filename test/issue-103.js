var assert = require("assert"),
	test = require('selenium-webdriver/testing'),
	webdriver = require('selenium-webdriver'),
	driver;

function randomString() {
	var randomness = Math.round(Math.random() * (99999-10000) + 10000); // [10000;99999]
	return new String(randomness);
}

var admin_username = "admin";
var admin_password = "never-use-this-in-production";
var regular_username = "this-is-a-veery-long-user-name";
var regular_password = "never-use-this-in-production";
var training_bit_imagepath = "/home/kraen/Billeder/bibtekkonf.jpg";


function signOut() {
	// Sign out
	driver.findElement(webdriver.By.id('logged-in-menu')).click();
	driver.findElement(webdriver.By.linkText('Sign out')).click();
}

function signIn() {
	// Go to the login page.
	driver.get("http://localhost:8000/user/login/");
	driver.findElement(webdriver.By.name('login')).sendKeys(regular_username);
	driver.findElement(webdriver.By.name('password')).sendKeys(regular_password);
	driver.findElement(webdriver.By.css('button[type=submit]')).click();
}

test.before(function() {
	driver = new webdriver.Builder().
		usingServer("http://localhost:9515/").
		withCapabilities(webdriver.Capabilities.chrome()).
		build();
	driver.manage().window().maximize();
	signIn();
});

test.after(function() {
	driver.quit();
});

function ensureNoOverlaps(elements) {
		var bounding_boxes = [];
		// A refresh breaks the grid.
		for(s in elements) {
			bounding_boxes[s] = {};
			var share = elements[s];
			var appendLocation = (function(s) { return function(location) {
				bounding_boxes[s].location = location;
			} })(s);
			var appendSize = (function(s) { return function(size) {
				bounding_boxes[s].size = size;
			} })(s);
			share.getLocation().then(appendLocation);
			share.getSize().then(appendSize);
		}
		driver.wait(function() {
			for(e in elements) {
				if (!bounding_boxes[e].location || !bounding_boxes[e].size)
					return false;
				return true;
			}
			// All locations and sizes are known.
		}, 1000).then(function() {
			var no_overlaps = true;
			for(b in bounding_boxes) {
				var box = bounding_boxes[b];
				for(a in bounding_boxes) {
					if(b === a) {
						continue; // Don't compare with itself.
					}
					var anotherBox = bounding_boxes[a];
					// box is to the left of another box.
					var isLeftOf = box.location.x + box.size.width < anotherBox.location.x,
						isRightOf = box.location.x > anotherBox.location.x + anotherBox.size.width,
						isAbove = box.location.y + box.size.height < anotherBox.location.y,
						isBelow = box.location.y > anotherBox.location.y + anotherBox.size.height;
					if(!isLeftOf && !isRightOf && !isAbove && !isBelow) {
						no_overlaps = false;
						console.error("Box "+b+" is overlapping box "+a);
					}

				}
			}
			assert.equal(no_overlaps, true);
		});
	}

// Check that no two shares overlap on the /shares page.
test.describe('The ability to see all shares without overlapping.', function() {

	test.it('Is not possible for two shares to overlap.', function() {
		//for(var i = 0; i < 10; i++) { // Try a couple of times.
		driver.get('http://localhost:8000/shares');
		driver.sleep(500);
		driver.findElements(webdriver.By.className("comment-compact")).then(ensureNoOverlaps);
		//};
	});
});