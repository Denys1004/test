# Generated by Django 2.2 on 2020-07-20 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log_reg_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='poster',
        ),
        migrations.AddField(
            model_name='job',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='executor', to='log_reg_app.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_num',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='category',
            name='job',
        ),
        migrations.AddField(
            model_name='category',
            name='job',
            field=models.ManyToManyField(related_name='categories', to='log_reg_app.Job'),
        ),
        migrations.AlterField(
            model_name='job',
            name='poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poster', to='log_reg_app.User'),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
