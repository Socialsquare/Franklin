var assert = require("assert"),
	utils = require('./test-utils');
	trainingBit = require('./training-bit-utils'),
	skill = require('./skill-utils');

before(function() {
	utils.before();
});

after(function() {
	utils.after();
});

// Check that no two shares overlap on the /shares page.
describe('draft-data and deleted data should not be present in statistics because it', function() {

	var created_training_bit;
	var created_skill;

	it('is possible for an admin to login', function(done) {
		utils.login_admin(done);
	});

	it('is possible for an admin to create a public training bit', function(done) {
		trainingBit.create(function(training_bit) {
			created_training_bit = training_bit;
			done();
		});
	});

	it('is possible for an admin to create a public skill', function(done) {
		skill.create(function(skill) {
			created_skill = skill;
			done();
		});
	});

	it('is possible for the admin to see statistics on the public skill', function(done) {
		browser
			.clickText('Trainer Dashboard')
			.clickText('See statistics')
			.clickText(created_skill.name, 'td')
			.clickText(created_training_bit.name, 'td', function() {
				done();
			});
	});

	it('is possible for an admin to draft a training bit', function(done) {
		browser
			.clickText('Trainer Dashboard')
			.clickText(created_training_bit.name)
			.click('#id_is_draft_1')
			.clickText('Save training bit', 'button', function() {
				done();
			});
	});

	it('is not possible for the admin to see statistics on the draft skill', function(done) {
		browser
			.clickText('Trainer Dashboard')
			.clickText('See statistics', 'a')
			.clickText(created_skill.name, 'td')
			.isVisibleText(created_training_bit.name, 'td', function(err, value) {
				assert(value !== true, "the training bit was visible");
				done();
			});
	});

	it('is possible for an admin to draft a skill', function(done) {
		browser
			.clickText('Trainer Dashboard')
			.clickText(created_skill.name)
			.click('#id_is_draft_1')
			.clickText('Save skill', 'button', function() {
				done();
			});
	});

	it('is not possible for the admin to see statistics on the draft skill', function(done) {
		browser
			.clickText('Trainer Dashboard')
			.clickText('See statistics', 'a')
			.isVisibleText(created_skill.name, 'td', function(err, value) {
				assert(value !== true, "the skill was visible");
				done();
			});
	});
});