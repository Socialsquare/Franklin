// Training
var utils = require('./test-utils'),
		path = require('path'),
		assert = require("assert");

var MAIL_DIRECTORY = "/tmp/gcl-messages";

exports.create = function( callback ) {
	var randomness = utils.random_string();
	user = {
		email: 'kh+'+randomness+'@bitblueprint.com',
		username: 'regular-'+randomness,
		password: 'never-use-this-in-production',
	};
	browser
		.appUrl('')
		.clickText('Sign up')
		.setValue('input[name=email]', user.email)
		.setValue('input[name=username]', user.username)
		.setValue('input[name=password1]', user.password)
		.setValue('input[name=password2]', user.password)
		.click('#terms-checkbox')
		.clickText('Sign Up', 'button', function() {
			// Receive the activation mail and activate the profile.
			utils.receiveMockedMail(function(activation_mail) {
				var link = activation_mail.match(/http:\/\/([^\/]*)\/user\/confirm-email\/([^\/]*)\//g);
				assert.notEqual(link, null);
				assert.equal(link.length > 0, true, "The link contains an activation link.");
				link = link[0];
				browser
					.url(link)
					.isVisibleText('Confirm E-mail Address', 'h1', function(err, value) {
						assert(value === true, "the welcome message didn't exist.");
						browser.click('button[type=submit]').call(function() {
							callback( user );
						});
					});

			});
		});
}