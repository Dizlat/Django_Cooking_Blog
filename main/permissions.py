from django.contrib.auth.mixins import UserPassesTestMixin


class UserHasPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.get_object().user == self.request.user