from django.core.management.base import BaseCommand
from apps.oaauth.models import OAUser,OADepartment

class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = OADepartment.objects.get(name='董事会')
        developer = OADepartment.objects.get(name='产品开发部')
        operator = OADepartment.objects.get(name='运营部')
        saler = OADepartment.objects.get(name='销售部')
        hr = OADepartment.objects.get(name='人事部')
        finance = OADepartment.objects.get(name='财务部')


        # 董事会员工 都是superuser用户
        # 1. jwj：属于董事会的leader
        jwj = OAUser.objects.create_superuser(email='jwj@qq.com',realname='江文杰',password='111111',
                                              department=boarder)
        # 2. zlm：董事会
        zlm = OAUser.objects.create_superuser(email='zlm@qq.com',realname='咋了嘛',password='111111',
                                              department=boarder)
        # 3. 张三：产品开发部leader
        zhangsan = OAUser.objects.create_user(email='zhangsan@qq.com',realname='张三',password='111111',
                                              department=developer)
        # 4. 李四：运营部leader
        lisi = OAUser.objects.create_user(email='lisi@qq.com', realname='李四', password='111111',
                                              department=operator)
        # 5. 王五：人事部leader
        wangwu = OAUser.objects.create_user(email='wangwu@qq.com', realname='王五', password='111111',
                                          department=hr)
        # 6. 赵六：财务部leader
        zhaoliu = OAUser.objects.create_user(email='zhaoliu@qq.com', realname='赵六', password='111111',
                                            department=finance)
        # 7. 孙七：销售部leader
        sunqi = OAUser.objects.create_user(email='sunqi@qq.com', realname='孙七', password='111111',
                                             department=saler)


        # 给各部门指定leader，manager
        # jwj：产品开发部 运营部 销售部
        # zlm：人事部 财务部
        # 董事会
        boarder.leader = jwj
        boarder.manager = None

        # 产品开发部
        developer.leader = zhangsan
        developer.manager = jwj

        # 运营部
        operator.leader = lisi
        operator.manager = jwj

        # 销售部
        saler.leader = sunqi
        saler.manager = jwj

        # 人事部
        hr.leader = wangwu
        hr.manager = zlm

        # 财务部
        finance.leader = zhaoliu
        finance.manager = zlm

        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()

        self.stdout.write('初始用户创建成功！')
