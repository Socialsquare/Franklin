from allauth.account.adapter import DefaultAccountAdapter
from django.core.urlresolvers import reverse
import datetime

JUST_NOW_SECONDS = 5

class AccountAdapter(DefaultAccountAdapter):

	def get_login_redirect_url(self, request):
		#timing = request.user.last_login - request.user.datetime_joined
		#joined_just_now = timing < datetime.timedelta(0, JUST_NOW_SECONDS)
		#welcome_completed
		if not request.user.has_been_welcomed:
			return reverse('new_user')
		else:
			return reverse('profile')