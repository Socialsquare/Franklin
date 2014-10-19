from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username, user_field
from allauth.utils import valid_email_or_none, generate_unique_username
from django.core.files.base import ContentFile
import requests

class SocialAccountAdapter(DefaultSocialAccountAdapter):
	def populate_user(self, request, sociallogin, data):
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		name = data.get('name')
		username = data.get('username')
		user = sociallogin.account.user
		# TODO: Consider using the super class for the stuff that is not unique to facebook!
		if sociallogin.account.provider == 'facebook':
			user_email(user, valid_email_or_none(email) or '')
			name_parts = (name or '').partition(' ')
			user_field(user, 'first_name', first_name or name_parts[0])
			user_field(user, 'last_name', last_name or name_parts[2])
			# Save a good username
			if username:
				username_suggestions = [username, first_name, last_name, email, 'user']
			else:
				username_suggestions = [first_name, last_name, email, 'user']
			user_username(user, generate_unique_username(username_suggestions))
			return user
		elif sociallogin.account.provider == 'twitter':
			if "screen_name" in sociallogin.account.extra_data.keys():
				username = sociallogin.account.extra_data['screen_name']
			user_email(user, valid_email_or_none(email) or '')
			name_parts = (name or '').partition(' ')
			user_field(user, 'first_name', first_name or name_parts[0])
			user_field(user, 'last_name', last_name or name_parts[2])
			# Save a good username
			if username:
				username_suggestions = [username, first_name, last_name, email, 'user']
			else:
				username_suggestions = [first_name, last_name, email, 'user']
			user_username(user, generate_unique_username(username_suggestions))
			return user
		elif sociallogin.account.provider == 'google':
			#if "screen_name" in sociallogin.account.extra_data.keys():
			#	username = sociallogin.account.extra_data['screen_name']
			user_email(user, valid_email_or_none(email) or '')
			name_parts = (name or '').partition(' ')
			user_field(user, 'first_name', first_name or name_parts[0])
			user_field(user, 'last_name', last_name or name_parts[2])
			if username:
				username_suggestions = [username, first_name, last_name, email, 'user']
			else:
				username_suggestions = [first_name, last_name, email, 'user']
			user_username(user, generate_unique_username(username_suggestions))
			return user
		else:
			return super(SocialAccountAdapter, self).populate_user(request, sociallogin, data)

	def save_user(self, request, sociallogin, form=None):
		user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
		if sociallogin.account.provider == 'facebook':
			# Profile picture!
			# Generate the Facebook image URL
			profile_picture_url = "http://graph.facebook.com/%s/picture?type=large" % sociallogin.account.uid
			# Download the Facebook profile image.
			profile_image_r = requests.get(profile_picture_url)
			profile_image_file = ContentFile(profile_image_r.content)
			# We have to use save=False, otherwise saving the image field saves the user model.
			user.image.save("%s.jpg" % sociallogin.account.uid, profile_image_file)

			# Gender
			if "gender" in sociallogin.account.extra_data.keys():
				gender = sociallogin.account.extra_data['gender']
				# Need to hang on to the userinfo object to save it.
				userinfo = user.userinfo
				if gender == "male" or gender == "female":
					userinfo.sex = gender
					userinfo.save()

			# Saving country
			if "locale" in sociallogin.account.extra_data.keys():
				locale = sociallogin.account.extra_data['locale']
				# Need to hang on to the userinfo object to save it.
				userinfo = user.userinfo
				locale = locale[locale.index('_') + 1:]
				userinfo.country = locale
				userinfo.save()

			descriptions = []
			# Creating a bio
			if "name" in sociallogin.account.extra_data.keys():
				name = sociallogin.account.extra_data['name']
				descriptions.append( "My name is %s." % name )
			if "location" in sociallogin.account.extra_data.keys():
				location = sociallogin.account.extra_data['location']
				descriptions.append( "I live in %s." % location['name'] )
			if "work" in sociallogin.account.extra_data.keys():
				works = sociallogin.account.extra_data['work']
				if len(works) > 0:
					work = works[0]
					employer = work['employer']
					descriptions.append( "I work at %s." % employer['name'] )
			user.description = "\n".join(descriptions)
			user.save()
		elif sociallogin.account.provider == 'twitter':
			# Saving the profile image
			# Profile picture!
			# Generate the Facebook image URL
			if "profile_image_url" in sociallogin.account.extra_data.keys():
				profile_picture_url = sociallogin.account.extra_data['profile_image_url']
				# Search/replace 'normal' for 400x400 in the profile image URL
				profile_picture_url = profile_picture_url.replace('normal', '400x400')
				# Download the Facebook profile image.
				profile_image_r = requests.get(profile_picture_url)
				profile_image_file = ContentFile(profile_image_r.content)
				# We have to use save=False, otherwise saving the image field saves the user model.
				user.image.save("%s.jpg" % sociallogin.account.uid, profile_image_file)
			# Saving the desciption
			if "description" in sociallogin.account.extra_data.keys():
				user.description = sociallogin.account.extra_data['description']
				user.description += "\nFollow me on Twitter: https://twitter.com/%s" % sociallogin.account.extra_data['screen_name']
			user.save()
		elif sociallogin.account.provider == 'google':
			# Generate the Facebook image URL
			if "picture" in sociallogin.account.extra_data.keys():
				profile_picture_url = sociallogin.account.extra_data['picture']
				# Download the Facebook profile image.
				profile_image_r = requests.get(profile_picture_url)
				profile_image_file = ContentFile(profile_image_r.content)
				# We have to use save=False, otherwise saving the image field saves the user model.
				user.image.save("%s.jpg" % sociallogin.account.uid, profile_image_file)

			# Gender
			if "gender" in sociallogin.account.extra_data.keys():
				gender = sociallogin.account.extra_data['gender']
				# Need to hang on to the userinfo object to save it.
				userinfo = user.userinfo
				if gender == "male" or gender == "female":
					userinfo.sex = gender
					userinfo.save()

			descriptions = []
			# Creating a bio
			if "name" in sociallogin.account.extra_data.keys():
				name = sociallogin.account.extra_data['name']
				descriptions.append( "My name is %s." % name )
			if "link" in sociallogin.account.extra_data.keys():
				link = sociallogin.account.extra_data['link']
				descriptions.append( "Visit my Google+ profile: %s" % link )
			user.description = "\n".join(descriptions)
			# Save the model!
			user.save()
		return user