var webdriver = require('selenium-webdriver'),
		fs = require('fs');

var admin_username = "admin";
var admin_password = "never-use-this-in-production";
var regular_username = "regular";
var regular_password = "never-use-this-in-production";

exports.BASE_URL = process.env.BASE_URL || 'http://localhost:8000/';
exports.MAIL_DIRECTORY = process.env.MAIL_DIRECTORY || '/tmp/gcl-messages';

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

	browser.appUrl = function(url) {
		return browser
			.url(exports.BASE_URL + url);
	}
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
		.url(exports.BASE_URL + "user/login/")
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
	return browser.appUrl(url);
}

exports.receiveMockedMail = function ( mail_callback ) {
	fs.readdir(exports.MAIL_DIRECTORY, function(err, files) {
		// Finding the newest mail.
		for(f in files) {
			var file = files[f];
			var file_path = exports.MAIL_DIRECTORY	 +"/"+ file;
			var file_stat = fs.statSync(file_path);
			var newest_file;
			var newest_file_ctime;
			if(!newest_file || newest_file.ctime < file_stat.ctime) {
				newest_file = f;
				newest_file_ctime = file_stat.ctime;
			}
		}
		// Finding the first link in the newest mail.
		var mail_file_path = exports.MAIL_DIRECTORY +"/"+ files[f];
		var mail_content = fs.readFileSync( mail_file_path, { encoding: 'utf8' } );
		mail_callback( mail_content );
	});
}

exports.assertNoOverlaps = function (elements) {
	// TODO: Test that no elements overlap.
}

/*
exports.ensureNoOverlaps = function (elements) {
		var bounding_boxes = [];
		// A refresh breaks the grid.
		for(e in elements) {
			bounding_boxes[s] = {};
			var element = elements[e];
			var appendLocation = (function(s) { return function(location) {
				bounding_boxes[s].location = location;
			} })(s);
			var appendSize = (function(s) { return function(size) {
				bounding_boxes[s].size = size;
			} })(s);
			element.getLocation().then(appendLocation);
			element.getSize().then(appendSize);
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
*/