# Generated by Django 4.1 on 2022-09-10 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userupgrade'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userupgrade',
            options={'verbose_name': 'Расширение', 'verbose_name_plural': 'Расширения'},
        ),
        migrations.AlterField(
            model_name='userupgrade',
            name='img',
            field=models.ImageField(default='media/profile-img/person-icon.png', upload_to='media/profile-img/'),
        ),
    ]