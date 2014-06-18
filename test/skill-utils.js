// Training
var utils = require('./test-utils');
var path = require('path');

exports.create = function( callback ) {
	var randomness = utils.random_string();
	skill = {
		name: 'Test Skill ' + randomness,
		image: path.resolve('global_change_lab/static/images/404.jpg'),
		description: 'This is the description of the test training ' + randomness,
	};
	return browser
		.clickText('Trainer Dashboard')
		.clickText('Add new skill')
		.setValue('input[name=name]', skill.name )
		.setValue('textarea[name=description]', skill.description )
		.dragAndDrop('#trainingbits-available-list li:first-child', '#trainingbits-chosen-list')
		.click('#id_is_draft_0')
		.clickText('Create new skill', 'button', function() {
			callback( skill );
		});
}