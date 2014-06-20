var assert = require("assert"),
	utils = require('./test-utils'),
	user = require('./user-utils');

before(function() {
	utils.before();
});

after(function() {
	utils.after();
});

// Check that no two shares overlap on the /shares page.
describe('Topics are not overlapping, because it', function() {

	var created_user;

	it('is possible to create a user', function(done) {
		user.create(function(user) {
			created_user = user;
			console.log("Created user "+user.username);
			done();
		});
	});

	it('is possible to fill out the profile', function(done) {
		browser
			.clickText('1/3 Next - update your profile')
			.click("#id_sex_1")
			.setValue('input[name=birthdate_0]', '01')
			.setValue('input[name=birthdate_1]', '01')
			.setValue('input[name=birthdate_2]', '1980')
			.click('select[name=country] option[value=DK]')
			.click('select[name=organization] option[value=other]')
			.setValue('textarea[name=description]', 'Some random description of the user ' + created_user.username)
			.clickText('2/3 Save - and choose your topics', 'button')
			.call(done);
	});

});