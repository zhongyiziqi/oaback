from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,PermissionsMixin,UserManager,BaseUserManager
from django.contrib.auth.hashers import make_password
from shortuuidfield import ShortUUIDField


class UserStatusChoice(models.IntegerChoices):
    # 已经激活
    ACTIVED = 1
    # 没有激活
    UNACTIVE = 2
    # 被锁定
    LOCKED = 3


# 创建OAUser模型
class OAUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, realname, email, password, **extra_fields):
        if not realname:
            raise ValueError("必须设置真实姓名")
        email = self.normalize_email(email)
        user = self.model(realname=realname, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, realname, email=None, password=None, **extra_fields):
        """
        创建普通用户
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(realname, email, password, **extra_fields)



    def create_superuser(self, realname, email=None, password=None, **extra_fields):
        """
        创建超级用户
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status",UserStatusChoice.ACTIVED)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级用户必须设置 is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级用户必须设置 is_superuser=True.")

        return self._create_user(realname, email, password, **extra_fields)




class OAUser(AbstractBaseUser, PermissionsMixin):
    """
    重写自定义User模型
    """
    uid = ShortUUIDField(primary_key=True)
    realname = models.CharField(max_length=150,unique=False)
    email = models.EmailField(unique=True, blank=False)
    telephone = models.CharField(max_length=20,blank=True)
    is_staff = models.BooleanField(default=True)
    # 只要关注status即可 无需关注is_active
    status = models.IntegerField(choices=UserStatusChoice,default=UserStatusChoice.UNACTIVE)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    department = models.ForeignKey('OADepartment',null=True,on_delete=models.SET_NULL,related_name='staffs',related_query_name='staffs')

    objects = OAUserManager()

    EMAIL_FIELD = "email"
    # USERNAME_FIELD是用来做鉴权的
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS：指定哪些字段时必须要传的，但是不能包括EMAIL_FIELD和USERNAME_FIELD已经设置过的值
    REQUIRED_FIELDS = ["realname","password"]


    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.realname

    def get_short_name(self):
        return self.realname

    # 排序
    # class Meta:
    #     ordering = ("-date_joined",)




class OADepartment(models.Model):
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=200)
    # leader一对一
    leader = models.OneToOneField(OAUser,null=True,on_delete=models.SET_NULL,related_name='leader_department',related_query_name='leader_department')
    # manager一对多
    manager = models.ForeignKey(OAUser,null=True,on_delete=models.SET_NULL,related_name='manage_departments',related_query_name='manage_departments')
