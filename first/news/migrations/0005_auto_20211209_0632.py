# Generated by Django 3.2.9 on 2021-12-09 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_news_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=25, verbose_name='Автор')),
                ('mail', models.EmailField(max_length=30, verbose_name='Электронная почта')),
                ('content', models.TextField(blank=True, verbose_name='Контент комментария')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name': 'Коммент',
                'verbose_name_plural': 'Комменты',
                'ordering': ['author'],
            },
        ),
        migrations.AddField(
            model_name='news',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='news.newscomment', verbose_name='Комментарий'),
        ),
    ]