# Generated by Django 4.2 on 2024-03-14 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_menu', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ('sort',), 'verbose_name': 'Пункт меню | Menu Point', 'verbose_name_plural': 'Пункты меню | Menu Points'},
        ),
        migrations.AddField(
            model_name='menuitem',
            name='css_class',
            field=models.CharField(blank=True, help_text='Можно задать, если пункту меню необходима особенная стилизация', max_length=100, null=True, verbose_name='CSS класс'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='subpage_url',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='URL подстраницы (при наличии)'),
        ),
    ]
