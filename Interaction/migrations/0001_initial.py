# Generated by Django 2.0 on 2020-07-06 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.IntegerField(verbose_name='选择的章节')),
                ('choiceid', models.IntegerField(verbose_name='具体id选择')),
                ('fatherid', models.IntegerField(verbose_name='父节点')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('bgmSound', models.IntegerField(verbose_name='背景音乐音量')),
                ('soundEffects', models.IntegerField(verbose_name='游戏音效音量')),
                ('dubbingSound', models.IntegerField(verbose_name='配音音量')),
            ],
        ),
        migrations.AddField(
            model_name='userchoice',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='Interaction.Users', verbose_name='user外键'),
        ),
    ]
