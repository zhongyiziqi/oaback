from django.shortcuts import render
from rest_framework import viewsets,mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Absent,AbsentType,AbsentStatusChoice
from .serializers import AbsentSerializer,AbsentTypeSerializer
from .utils import get_responder
from apps.oaauth.serializers import UserSerializer

# Create your views here.
# 1.发起考勤(create)
# 2,处理考勤(update)
# 3.查看自己的考勤列表(list?who=my)
# 4.查看下属的考勤列表(list?who=sub)
class AbsentViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        # 默认情况下，如果要修改某一条数据，那么要把这个数据的序列化中指定的字段都上传
        # 如果想只修改一部分数据，那么可以在kwargs中设置partial为True
        kwargs['partial'] = True
        return super().update(request,*args,**kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # 从request中获取当前想要的是谁的考勤列表
        who = request.query_params.get('who')
        if who and who == 'sub':
            result = queryset.filter(responder=request.user)
        else:
            result = queryset.filter(requester=request.user)
        # 分页 paginate_queryset会做分页的逻辑处理
        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(result,many=True)
        return Response(data=serializer.data)


# 1. 请假类型
class AbsentTypeView(APIView):
    def get(self,request):
        types = AbsentType.objects.all()
        serializer = AbsentTypeSerializer(types,many=True)
        return Response(data=serializer.data)

# 2.显示审批者
class ResponderView(APIView):
    def get(self,request):
        responder = get_responder(request)
        serializer = UserSerializer(responder)
        return Response(data=serializer.data)