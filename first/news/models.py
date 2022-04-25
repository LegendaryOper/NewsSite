from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=150,verbose_name='Наименование')
    content = models.TextField(blank=True,verbose_name='Контент')
    created_at= models.DateTimeField(auto_now_add=True,verbose_name='Создано')
    updated_at=models.DateTimeField(auto_now=True,verbose_name='Изменено')
    photo=models.ImageField(upload_to='photos/%Y/%m%d/',blank=True,verbose_name='Фото')
    is_publishied=models.BooleanField(default=True,verbose_name='Опубликовано')
    category=models.ForeignKey('Category',models.PROTECT,blank=True,verbose_name='Категория')
    views = models.IntegerField(default=0)


    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk, })

    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Новость'
        verbose_name_plural = 'Новости'
        ordering=['-created_at']


class Category(models.Model):
    title=models.CharField(max_length=150,db_index=True,verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse('category',kwargs={'category_id':self.pk,})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'
        ordering=['title']


class NewsComment(models.Model):
    author = models.CharField(max_length=25, verbose_name='Автор')
    mail = models.EmailField(max_length=30, verbose_name='Электронная почта')
    content = models.TextField(blank=True,verbose_name='Контент комментария')
    created_at=models.DateTimeField(auto_now_add=True,verbose_name='Создано')
    news_id = models.ForeignKey('News', models.PROTECT, null=True, blank=True, verbose_name='ID новости')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'
        ordering = ['author']




