# Generated by Django 2.2 on 2020-08-14 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import omformflow.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=200)),
                ('updatetime', models.DateTimeField(blank=True, null=True, verbose_name='更新時間')),
                ('version', models.IntegerField(blank=True, null=True, verbose_name='流程版本')),
                ('app_attr', models.CharField(max_length=100, verbose_name='屬性')),
                ('undeploy_flag', models.BooleanField(default=False, verbose_name='下線')),
                ('language_package', models.TextField(default='{}', verbose_name='語言包')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='OmParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True, verbose_name='參數名稱')),
                ('value', models.TextField(blank=True, null=True, verbose_name='參數值')),
                ('type', models.TextField(blank=True, null=True, verbose_name='類型')),
                ('description', models.TextField(blank=True, null=True, verbose_name='說明')),
                ('shadow', models.BooleanField(default=False, verbose_name='是否遮蔽')),
                ('group_id', models.TextField(blank=True, null=True, verbose_name='群組id')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SLARule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sla_name', models.CharField(max_length=200, verbose_name='服務水準名稱')),
                ('description', models.TextField(blank=True, null=True, verbose_name='說明')),
                ('app_name', models.CharField(max_length=200, verbose_name='應用名稱')),
                ('flow_name', models.CharField(max_length=200, verbose_name='流程名稱')),
                ('flow_uuid', models.UUIDField(blank=True, null=True, verbose_name='流程編號')),
                ('type', models.TextField(blank=True, null=True, verbose_name='類型')),
                ('timer_start', models.TextField(blank=True, null=True, verbose_name='時間測量開始')),
                ('timer_end', models.TextField(blank=True, null=True, verbose_name='時間測量終止')),
                ('advanced', models.TextField(blank=True, null=True, verbose_name='進階條件')),
                ('target', models.TextField(blank=True, null=True, verbose_name='數值測量欄位')),
                ('remind', models.TextField(blank=True, null=True, verbose_name='提醒')),
                ('violation', models.TextField(blank=True, null=True, verbose_name='違反')),
                ('title', models.TextField(blank=True, null=True, verbose_name='標題')),
                ('content', models.TextField(blank=True, null=True, verbose_name='內容')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('notify_createuser', models.BooleanField(default=False, verbose_name='通知開單人')),
                ('notify_group', models.TextField(blank=True, null=True, verbose_name='通知角色')),
                ('notify_user', models.TextField(blank=True, null=True, verbose_name='通知人')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='WorkspaceApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=200)),
                ('updatetime', models.DateTimeField(blank=True, null=True, verbose_name='更新時間')),
                ('active_app_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='對應名稱')),
                ('app_attr', models.CharField(max_length=100, verbose_name='屬性')),
                ('language_package', models.TextField(default='{}', verbose_name='語言包')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('OmFormFlow_Manage', '自訂流程管理'),),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SLAData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(default='num', verbose_name='類型')),
                ('app_name', models.CharField(max_length=200, verbose_name='應用名稱')),
                ('flow_name', models.CharField(max_length=200, verbose_name='流程名稱')),
                ('data_no', models.IntegerField(blank=True, null=True, verbose_name='資料編號')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('remind', models.TextField(blank=True, null=True, verbose_name='提醒')),
                ('violation', models.TextField(blank=True, null=True, verbose_name='違反')),
                ('level', models.CharField(default='green', max_length=50, verbose_name='燈號')),
                ('closed', models.BooleanField(default=False, verbose_name='關閉標記')),
                ('sla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omformflow.SLARule')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='OmdataWorklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_uuid', models.UUIDField(blank=True, null=True, verbose_name='流程編號')),
                ('data_no', models.IntegerField(blank=True, null=True, verbose_name='資料流水號')),
                ('content', models.TextField(blank=True, null=True, verbose_name='內容')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_worklog', to=settings.AUTH_USER_MODEL, verbose_name='建立人')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='OmdataRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_flow', models.UUIDField(blank=True, null=True, verbose_name='主表單流程')),
                ('subject_no', models.IntegerField(blank=True, null=True, verbose_name='主資料編號')),
                ('relation_type', models.TextField(blank=True, null=True, verbose_name='關聯類型')),
                ('relation_percentage', models.IntegerField(blank=True, null=True, verbose_name='被影響百分比')),
                ('object_flow', models.UUIDField(blank=True, null=True, verbose_name='副表單流程')),
                ('object_no', models.IntegerField(blank=True, null=True, verbose_name='副資料編號')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='建立人員')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='OmdataFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=omformflow.models.get_file_path)),
                ('size', models.IntegerField(blank=True, verbose_name='大小')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('delete', models.BooleanField(default=False, verbose_name='是否刪除')),
                ('file_name', models.TextField(blank=True, null=True, verbose_name='檔案名稱')),
                ('flow_uuid', models.UUIDField(blank=True, null=True, verbose_name='流程編號')),
                ('data_no', models.IntegerField(blank=True, null=True, verbose_name='資料流水號')),
                ('data_id', models.IntegerField(blank=True, null=True, verbose_name='資料編號')),
                ('upload_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_omdatefile', to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='上傳人員')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='FlowWorkspace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_name', models.CharField(max_length=200, verbose_name='名稱')),
                ('description', models.TextField(blank=True, null=True, verbose_name='說明')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('formobject', models.TextField(blank=True, null=True, verbose_name='流程表單設計')),
                ('flowobject', models.TextField(blank=True, null=True, verbose_name='流程設計')),
                ('config', models.TextField(blank=True, null=True, verbose_name='流程設定')),
                ('subflow', models.TextField(blank=True, null=True, verbose_name='子流程')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('flow_app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omformflow.WorkspaceApplication')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='FlowActive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_uuid', models.UUIDField(blank=True, null=True, verbose_name='流程編號')),
                ('flow_uid', models.TextField(blank=True, null=True, verbose_name='uid')),
                ('version', models.IntegerField(blank=True, null=True, verbose_name='流程版本')),
                ('parent_uuid', models.UUIDField(blank=True, null=True, verbose_name='主流程編號')),
                ('attr', models.TextField(blank=True, null=True, verbose_name='屬性')),
                ('is_active', models.BooleanField(default=True, verbose_name='啟用/停用')),
                ('flow_name', models.CharField(max_length=200, verbose_name='名稱')),
                ('description', models.TextField(blank=True, null=True, verbose_name='說明')),
                ('deploytime', models.DateTimeField(auto_now_add=True, verbose_name='部署時間')),
                ('undeploy_flag', models.BooleanField(default=False, verbose_name='下線')),
                ('undeploy_time', models.DateTimeField(blank=True, null=True, verbose_name='下線時間')),
                ('formobject', models.TextField(blank=True, null=True, verbose_name='流程表單設計')),
                ('merge_formobject', models.TextField(blank=True, null=True, verbose_name='整合表單設計')),
                ('flowobject', models.TextField(blank=True, null=True, verbose_name='流程設計')),
                ('formcounter', models.CharField(blank=True, max_length=200, null=True, verbose_name='表單計數')),
                ('flowcounter', models.CharField(blank=True, max_length=200, null=True, verbose_name='流程計數')),
                ('title_field', models.CharField(blank=True, max_length=500, null=True, verbose_name='標題欄位')),
                ('status_field', models.CharField(blank=True, max_length=500, null=True, verbose_name='狀態欄位')),
                ('common', models.BooleanField(default=False, verbose_name='共用')),
                ('flowlog', models.BooleanField(default=False, verbose_name='執行過程紀錄')),
                ('api', models.BooleanField(default=False, verbose_name='應用程式介面')),
                ('fp_show', models.BooleanField(default=False, verbose_name='查看目前流程及進度')),
                ('attachment', models.BooleanField(default=False, verbose_name='附加檔案功能')),
                ('relation', models.BooleanField(default=False, verbose_name='顯示關聯資料')),
                ('worklog', models.BooleanField(default=False, verbose_name='填寫及顯示工作日誌')),
                ('history', models.BooleanField(default=False, verbose_name='操作歷程')),
                ('mission', models.BooleanField(default=True, verbose_name='建立任務')),
                ('display_field', models.TextField(blank=True, null=True, verbose_name='要顯示的欄位')),
                ('search_field', models.TextField(blank=True, null=True, verbose_name='要查詢的欄位')),
                ('action1', models.TextField(blank=True, null=True, verbose_name='快速操作1')),
                ('action2', models.TextField(blank=True, null=True, verbose_name='快速操作2')),
                ('type', models.TextField(blank=True, null=True, verbose_name='分類')),
                ('permission', models.TextField(blank=True, null=True, verbose_name='權限')),
                ('api_path', models.CharField(blank=True, max_length=500, null=True, verbose_name='api路徑')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('flow_app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omformflow.ActiveApplication')),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]
