# Generated by Django 2.0.3 on 2019-04-07 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20190405_2221'),
        ('group', '0007_auto_20190406_0846'),
    ]

    operations = [
        migrations.CreateModel(
            name='group_affiliation_archive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changedat', models.TimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.Group')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Usertype')),
            ],
        ),
    ]
