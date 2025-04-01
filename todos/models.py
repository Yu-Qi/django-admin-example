from django.db import models
from django.core.validators import URLValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分類'
        verbose_name_plural = '分類'

class Todo(models.Model):
    title = models.CharField(max_length=200, verbose_name='標題')
    description = models.TextField(blank=True, verbose_name='描述')
    url = models.URLField(blank=True, validators=[URLValidator()], verbose_name='相關連結')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='todos', verbose_name='分類')
    completed = models.BooleanField(default=False, verbose_name='已完成')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = '待辦事項'
        verbose_name_plural = '待辦事項'
