# Generated by Django 2.2 on 2020-08-14 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ommessage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('omuser', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_user_username', models.CharField(blank=True, max_length=100, verbose_name='發送者名稱')),
                ('create_group_name', models.CharField(blank=True, max_length=100, verbose_name='發送群組名稱')),
                ('delete_users_username', models.TextField(blank=True, verbose_name='已刪除的接收者名稱')),
                ('receive_groups_name', models.TextField(blank=True, verbose_name='接收群組名稱')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('content', models.TextField(blank=True, verbose_name='內文')),
                ('create_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='omuser.OmGroup')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='主旨')),
                ('formid', models.CharField(blank=True, max_length=100, verbose_name='表單編號')),
                ('dataid', models.CharField(blank=True, max_length=100, verbose_name='資料編號')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='更新時間')),
                ('flag', models.BooleanField(default=False, verbose_name='標記')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='MessageHistoryFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=ommessage.models.get_file_path)),
                ('size', models.IntegerField(blank=True, verbose_name='大小')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('delete', models.BooleanField(default=False, verbose_name='是否刪除')),
                ('main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ommessage.MessageHistory')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='messagehistory',
            name='messages',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ommessage.Messages'),
        ),
        migrations.CreateModel(
            name='MessageBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False, verbose_name='是否讀取')),
                ('delete', models.BooleanField(default=False, verbose_name='是否刪除')),
                ('messagehistory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ommessage.MessageHistory')),
                ('messages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ommessage.Messages')),
                ('omuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='HistoryMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messagehistory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ommessage.MessageHistory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='HistoryGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omuser.OmGroup')),
                ('messagehistory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ommessage.MessageHistory')),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]
