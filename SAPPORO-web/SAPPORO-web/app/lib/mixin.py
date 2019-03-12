# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


class MyLoginRequiredMixin(LoginRequiredMixin):
    raise_excrption = True
    permission_denied_message = "You do not have permission to access this page."

    def handle_not_authenticated(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def handle_exception(self):
        raise PermissionDenied(self.get_permission_denied_message())

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_not_authenticated()
        if self.raise_exception():
            return self.handle_exception()
        return super().dispatch(request, *args, **kwargs)
