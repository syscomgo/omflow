# Generated by Django 3.1.5 on 2021-02-23 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('omformflow', '0003_auto_20210126_1907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workspaceapplication',
            options={'default_permissions': (), 'permissions': (('OmFormFlow_Manage', 'تخصيص ادارة التدفق'),)},
        ),
        migrations.AlterField(
            model_name='activeapplication',
            name='app_attr',
            field=models.CharField(max_length=100, verbose_name='اعدادات'),
        ),
        migrations.AlterField(
            model_name='activeapplication',
            name='language_package',
            field=models.TextField(default='{}', verbose_name='اللغة'),
        ),
        migrations.AlterField(
            model_name='activeapplication',
            name='undeploy_flag',
            field=models.BooleanField(default=False, verbose_name='غير متصل'),
        ),
        migrations.AlterField(
            model_name='activeapplication',
            name='updatetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تحديث الوقت'),
        ),
        migrations.AlterField(
            model_name='activeapplication',
            name='version',
            field=models.IntegerField(blank=True, null=True, verbose_name='اصدار التدفق'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='action1',
            field=models.TextField(blank=True, null=True, verbose_name='عملية سريعة1'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='action2',
            field=models.TextField(blank=True, null=True, verbose_name='عملية سريعة2'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='api',
            field=models.BooleanField(default=False, verbose_name='الواجهة'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='api_path',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='عنوان الواجهة'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='attachment',
            field=models.BooleanField(default=False, verbose_name='المرفق'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='attr',
            field=models.TextField(blank=True, null=True, verbose_name='اعدادات'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='common',
            field=models.BooleanField(default=False, verbose_name='المشاركة'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='deploytime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='وقت النشر'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='وصف التدفق'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='display_field',
            field=models.TextField(blank=True, null=True, verbose_name='العمود الذي سيتم عرضه'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='flow_name',
            field=models.CharField(max_length=200, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='flow_uid',
            field=models.TextField(blank=True, null=True, verbose_name='رقم واجهة المستخدم'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='flow_uuid',
            field=models.UUIDField(blank=True, null=True, verbose_name='رقم التدفق'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='flowcounter',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='عدد التدفقات'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='flowlog',
            field=models.BooleanField(default=False, verbose_name='السجل'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='flowobject',
            field=models.TextField(blank=True, null=True, verbose_name='تصميم النموذج'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='formcounter',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='عدد النماذج'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='formobject',
            field=models.TextField(blank=True, null=True, verbose_name='تصميم تدفق النموذح'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='fp_show',
            field=models.BooleanField(default=False, verbose_name='عرض حالة التدفق'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='history',
            field=models.BooleanField(default=False, verbose_name='تاريخ العمليات'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='التمكين/عدم التمكين'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='merge_formobject',
            field=models.TextField(blank=True, null=True, verbose_name='التصميم المدمج للنموذج'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='mission',
            field=models.BooleanField(default=True, verbose_name='انشاء المهمة'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='parent_uuid',
            field=models.UUIDField(blank=True, null=True, verbose_name='رقم التدفق الرئيسي'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='permission',
            field=models.TextField(blank=True, null=True, verbose_name='الاذن'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='relation',
            field=models.BooleanField(default=False, verbose_name='عرض المعلومات المتصلة'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='search_field',
            field=models.TextField(blank=True, null=True, verbose_name='الحقل المستعلم عنه'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='status_field',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='اسم الحالة'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='title_field',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='اسم الحقل'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='type',
            field=models.TextField(blank=True, null=True, verbose_name='التصنيف'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='undeploy_flag',
            field=models.BooleanField(default=False, verbose_name='غير متصل'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='undeploy_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='وقت عدم الاتصال'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='version',
            field=models.IntegerField(blank=True, null=True, verbose_name='اصدار التدفق'),
        ),
        migrations.AlterField(
            model_name='flowactive',
            name='worklog',
            field=models.BooleanField(default=False, verbose_name='اليومية'),
        ),
        migrations.AlterField(
            model_name='flowworkspace',
            name='config',
            field=models.TextField(blank=True, null=True, verbose_name='خصائص التدفق'),
        ),
        migrations.AlterField(
            model_name='flowworkspace',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='انشاء الوقت'),
        ),
        migrations.AlterField(
            model_name='flowworkspace',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='وصف التدفق'),
        ),
        migrations.AlterField(
            model_name='flowworkspace',
            name='flow_name',
            field=models.CharField(max_length=200, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='flowworkspace',
            name='flowobject',
            field=models.TextField(blank=True, null=True, verbose_name='تصميم النموذج'),
        ),
        migrations.AlterField(
            model_name='flowworkspace',
            name='formobject',
            field=models.TextField(blank=True, null=True, verbose_name='تصميم تدفق النموذح'),
        ),
        migrations.AlterField(
            model_name='flowworkspace',
            name='subflow',
            field=models.TextField(blank=True, null=True, verbose_name='التدفق الفرعي'),
        ),
        migrations.AlterField(
            model_name='flowworkspace',
            name='updatetime',
            field=models.DateTimeField(auto_now=True, verbose_name='تحديث الوقت'),
        ),
        migrations.AlterField(
            model_name='omdatafiles',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='انشاء الوقت'),
        ),
        migrations.AlterField(
            model_name='omdatafiles',
            name='data_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='رقم البيانات'),
        ),
        migrations.AlterField(
            model_name='omdatafiles',
            name='data_no',
            field=models.IntegerField(blank=True, null=True, verbose_name='الرقم المسلسل للبيانات'),
        ),
        migrations.AlterField(
            model_name='omdatafiles',
            name='delete',
            field=models.BooleanField(default=False, verbose_name='حذف ام عدم حذف'),
        ),
        migrations.AlterField(
            model_name='omdatafiles',
            name='file_name',
            field=models.TextField(blank=True, null=True, verbose_name='اسم الملف'),
        ),
        migrations.AlterField(
            model_name='omdatafiles',
            name='flow_uuid',
            field=models.UUIDField(blank=True, null=True, verbose_name='رقم التدفق'),
        ),
        migrations.AlterField(
            model_name='omdatafiles',
            name='size',
            field=models.IntegerField(blank=True, verbose_name='المقاس'),
        ),
        migrations.AlterField(
            model_name='omdatafiles',
            name='upload_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_omdatefile', to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='تحميل الشخص'),
        ),
        migrations.AlterField(
            model_name='omdatarelation',
            name='create_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='التوظيف'),
        ),
        migrations.AlterField(
            model_name='omdatarelation',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='انشاء الوقت'),
        ),
        migrations.AlterField(
            model_name='omdatarelation',
            name='object_flow',
            field=models.UUIDField(blank=True, null=True, verbose_name='التدفق الثاني للفورمة'),
        ),
        migrations.AlterField(
            model_name='omdatarelation',
            name='object_no',
            field=models.IntegerField(blank=True, null=True, verbose_name='رقم البيانات الفرعية'),
        ),
        migrations.AlterField(
            model_name='omdatarelation',
            name='relation_percentage',
            field=models.IntegerField(blank=True, null=True, verbose_name='نسبة التأثير'),
        ),
        migrations.AlterField(
            model_name='omdatarelation',
            name='relation_type',
            field=models.TextField(blank=True, null=True, verbose_name='نوع الرابطة'),
        ),
        migrations.AlterField(
            model_name='omdatarelation',
            name='subject_flow',
            field=models.UUIDField(blank=True, null=True, verbose_name='النموذج الرئيسي لتدفق النموذج'),
        ),
        migrations.AlterField(
            model_name='omdatarelation',
            name='subject_no',
            field=models.IntegerField(blank=True, null=True, verbose_name='رقم المعلومات الرئيسية'),
        ),
        migrations.AlterField(
            model_name='omdataworklog',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='محتوي'),
        ),
        migrations.AlterField(
            model_name='omdataworklog',
            name='create_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_worklog', to=settings.AUTH_USER_MODEL, verbose_name='انشاء'),
        ),
        migrations.AlterField(
            model_name='omdataworklog',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='انشاء الوقت'),
        ),
        migrations.AlterField(
            model_name='omdataworklog',
            name='data_no',
            field=models.IntegerField(blank=True, null=True, verbose_name='الرقم المسلسل للبيانات'),
        ),
        migrations.AlterField(
            model_name='omdataworklog',
            name='flow_uuid',
            field=models.UUIDField(blank=True, null=True, verbose_name='رقم التدفق'),
        ),
        migrations.AlterField(
            model_name='omparameter',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='وصف التدفق'),
        ),
        migrations.AlterField(
            model_name='omparameter',
            name='group_id',
            field=models.TextField(blank=True, null=True, verbose_name='رقم المجموعة'),
        ),
        migrations.AlterField(
            model_name='omparameter',
            name='name',
            field=models.TextField(blank=True, null=True, verbose_name='اسم المعامل'),
        ),
        migrations.AlterField(
            model_name='omparameter',
            name='shadow',
            field=models.BooleanField(default=False, verbose_name='هل هناك تغطية'),
        ),
        migrations.AlterField(
            model_name='omparameter',
            name='type',
            field=models.TextField(blank=True, null=True, verbose_name='النوع'),
        ),
        migrations.AlterField(
            model_name='omparameter',
            name='value',
            field=models.TextField(blank=True, null=True, verbose_name='قيمة المعامل'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='app_name',
            field=models.CharField(max_length=200, verbose_name='اسم التطبيق'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='closed',
            field=models.BooleanField(default=False, verbose_name='اغلاق العلامة'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='انشاء الوقت'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='data_no',
            field=models.IntegerField(blank=True, null=True, verbose_name='رقم البيانات'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='flow_name',
            field=models.CharField(max_length=200, verbose_name='اسم التدفق'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='level',
            field=models.CharField(default='green', max_length=50, verbose_name='مستوي'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='remind',
            field=models.TextField(blank=True, null=True, verbose_name='تذكير'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='type',
            field=models.TextField(default='num', verbose_name='النوع'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='updatetime',
            field=models.DateTimeField(auto_now=True, verbose_name='تحديث الوقت'),
        ),
        migrations.AlterField(
            model_name='sladata',
            name='violation',
            field=models.TextField(blank=True, null=True, verbose_name='انتهاك'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='advanced',
            field=models.TextField(blank=True, null=True, verbose_name='حالات متقدمة'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='app_name',
            field=models.CharField(max_length=200, verbose_name='اسم التطبيق'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='محتوي'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='انشاء الوقت'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='وصف التدفق'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='flow_name',
            field=models.CharField(max_length=200, verbose_name='اسم التدفق'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='flow_uuid',
            field=models.UUIDField(blank=True, null=True, verbose_name='رقم التدفق'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='notify_createuser',
            field=models.BooleanField(default=False, verbose_name='اعلام المنشيء'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='notify_group',
            field=models.TextField(blank=True, null=True, verbose_name='اعلام القواعد'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='notify_user',
            field=models.TextField(blank=True, null=True, verbose_name='إعلام المنستخدم '),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='remind',
            field=models.TextField(blank=True, null=True, verbose_name='تذكير'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='sla_name',
            field=models.CharField(max_length=200, verbose_name='إسم SLA'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='target',
            field=models.TextField(blank=True, null=True, verbose_name='حقل قياس رقمي'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='timer_end',
            field=models.TextField(blank=True, null=True, verbose_name='وقت انتهاء القياس'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='timer_start',
            field=models.TextField(blank=True, null=True, verbose_name='بداية وقت القياس'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='title',
            field=models.TextField(blank=True, null=True, verbose_name='مسمي'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='type',
            field=models.TextField(blank=True, null=True, verbose_name='النوع'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='updatetime',
            field=models.DateTimeField(auto_now=True, verbose_name='تحديث الوقت'),
        ),
        migrations.AlterField(
            model_name='slarule',
            name='violation',
            field=models.TextField(blank=True, null=True, verbose_name='انتهاك'),
        ),
        migrations.AlterField(
            model_name='workspaceapplication',
            name='active_app_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='الاسم متقاطع'),
        ),
        migrations.AlterField(
            model_name='workspaceapplication',
            name='app_attr',
            field=models.CharField(max_length=100, verbose_name='اعدادات'),
        ),
        migrations.AlterField(
            model_name='workspaceapplication',
            name='language_package',
            field=models.TextField(default='{}', verbose_name='اللغة'),
        ),
        migrations.AlterField(
            model_name='workspaceapplication',
            name='updatetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='تحديث الوقت'),
        ),
    ]
