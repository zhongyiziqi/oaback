from rest_framework import serializers
from .models import OAUser,UserStatusChoice,OADepartment
from rest_framework import exceptions

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,error_messages={"required":"请输入邮箱！"})
    password = serializers.CharField(max_length=20,min_length=6)

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # 通过邮箱查找用户
            user = OAUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("请传入正确邮箱！")
            if not user.check_password(password):
                raise serializers.ValidationError("请传入正确密码！")
            if user.status == UserStatusChoice.UNACTIVE:
                raise serializers.ValidationError("该用户未激活！")
            elif user.status == UserStatusChoice.LOCKED:
                raise serializers.ValidationError("该用户被锁定！")
            # 为了节省执行SQL语句的次数，这里把User直接放到attrs中，方便在视图中使用
            attrs['user'] = user
        else:
            raise serializers.ValidationError("请输入邮箱和密码！")
        return attrs

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = OAUser
        # fields = "__all__"
        exclude = ('password','groups','user_permissions')



class ResetPwdSerializer(serializers.Serializer):
    oldpwd = serializers.CharField(min_length=6,max_length=20)
    pwd1 = serializers.CharField(min_length=6,max_length=20)
    pwd2 = serializers.CharField(min_length=6,max_length=20)
    def validate(self, attrs):
        oldpwd = attrs['oldpwd']
        pwd1 = attrs['pwd1']
        pwd2 = attrs['pwd2']
        user = self.context['request'].user
        if not user.check_password(oldpwd):
            raise exceptions.ValidationError("旧密码错误!")
        if pwd1 != pwd2:
            raise exceptions.ValidationError("密码不一致！")
        return attrs