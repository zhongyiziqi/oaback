from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework.status import HTTP_403_FORBIDDEN
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse


OAUser = get_user_model()

class LoginCheckMiddleware(MiddlewareMixin):
    keyword = "JWT"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.white_list=[reverse("oaauth:login"),reverse("staff:active_staff")]


    def process_view(self,request,view_func,view_args,view_kwargs):
        # 1.如果返回None,那么会正常执行（包括执行视图、执行其他中间件的代码）
        # 2.如果返回一个HttpResponse对象，那么将不会执行视图，以及后面的中间件代码
        if request.path in self.white_list or request.path.startswith(settings.MEDIA_URL):
            request.user = AnonymousUser()
            request.auth = None
            return None
        try:
            auth = get_authorization_header(request).split()

            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.ValidationError("请传入JWT!")

            if len(auth) == 1:
                msg = '没有提供JWToken！'
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = '无效的JWT！'
                raise exceptions.AuthenticationFailed(msg)

            try:
                # 解密的算法和key必须和加密的算法保持一致
                jwt_token = auth[1]
                payload = jwt.decode(jwt_token, key=settings.SECRET_KEY, algorithms="HS256")
                userid = payload.get('userid')
                try:
                    user = OAUser.objects.get(pk=userid)
                    request.user = user
                    request.auth = jwt_token
                except Exception:
                    msg = '用户信息错误！'
                    raise exceptions.AuthenticationFailed(msg)

            except jwt.ExpiredSignatureError:
                msg = 'token已过期！'
                raise exceptions.AuthenticationFailed(msg)
        except Exception as e:
            print(e)
            return JsonResponse(data={"detail":"请先登录"},status=HTTP_403_FORBIDDEN)