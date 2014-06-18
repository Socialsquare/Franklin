// Training
var utils = require('./test-utils');
var path = require('path');

exports.create = function( callback ) {
	var randomness = utils.random_string();
	training_bit = {
		name: 'Test Training Bit ' + randomness,
		image: path.resolve('global_change_lab/static/images/404.jpg'),
		description: 'This is the description of the test training ' + randomness,
	};
	return browser
		.clickText('Trainer Dashboard')
		.clickText('Add new training bit')
		.setValue('input[name=name]', training_bit.name )
		.chooseFile('input[name=image]', training_bit.image )
		.setValue('textarea[name=description]', training_bit.description )
		.click('#id_is_draft_0')
		.clickText('Create new training bit', 'button', function() {
			callback( training_bit );
		});
}