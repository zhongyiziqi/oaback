from rest_framework import serializers
from .models import Inform,InformRead
from apps.oaauth.serializers import UserSerializer,DepartmentSerializer
from apps.oaauth.models import OADepartment


class InformReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformRead
        fields = "__all__"

class InformSerialzer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    departments = DepartmentSerializer(many=True,read_only=True)
    # department_ids:是一个包含了部门id的列表
    # 如果后端要接受列表，那么就需要用到ListField
    department_ids = serializers.ListField(write_only=True)
    reads = InformReadSerializer(many=True,read_only=True)

    class Meta:
        model = Inform
        fields = "__all__"
        read_only_fields = ('public',)

    def create(self, validated_data):
        request = self.context['request']
        department_ids = validated_data.pop("department_ids")
        department_ids = list(map(lambda value:int(value),department_ids))

        if 0 in department_ids:
            inform = Inform.objects.create(public=True,author=request.user,**validated_data)
        else:
            departments = OADepartment.objects.filter(id__in=department_ids).all()
            inform = Inform.objects.create(public=False,author=request.user,**validated_data)
            inform.departments.set(departments)
            inform.save()
        return inform


class ReadInformSerializer(serializers.Serializer):
    inform_pk = serializers.IntegerField(error_messages={"required":'请传入inform的id！'})