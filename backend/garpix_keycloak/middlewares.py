from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import login, authenticate, get_user_model
from garpix_utils.logs.enums.get_enums import Action, ActionResult
from garpix_utils.logs.loggers import ib_logger
from garpix_utils.logs.services.logger_iso import LoggerIso


class KeycloakAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):

        request_data = request.GET

        if not request.user.is_authenticated and 'keycloak_state' in request.session and 'state' in request_data and 'code' in request_data and request_data.get(
                'state') == request.session['keycloak_state']:

            user = authenticate(request)
            if user and not getattr(user, 'is_blocked', False):
                login(request, user)

                message = f'Пользователь {user.username} вошел в систему.'

                log = ib_logger.create_log(action=Action.user_login.value,
                                           obj=get_user_model().__name__,
                                           obj_address=request.path,
                                           result=ActionResult.success,
                                           sbj=user.username,
                                           sbj_address=LoggerIso.get_client_ip(request),
                                           msg=message)

                ib_logger.write_string(log)
