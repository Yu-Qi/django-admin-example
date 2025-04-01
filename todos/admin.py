from django.contrib import admin
from django.db.models import Count, Q
from django.db.models.functions import TruncDay, TruncHour
from django.utils import timezone
from django.urls import path, reverse
from django.template.response import TemplateResponse
from .models import Todo, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'todo_count', 'completed_count', 'created_at')
    search_fields = ('name',)

    def todo_count(self, obj):
        return obj.todos.count()
    todo_count.short_description = '待辦事項數量'

    def completed_count(self, obj):
        return obj.todos.filter(completed=True).count()
    completed_count.short_description = '已完成數量'

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completed', 'created_at', 'updated_at')
    list_filter = ('completed', 'category', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    change_list_template = 'admin/todos/todo/change_list.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='todo_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        # 基本統計
        total_todos = Todo.objects.count()
        completed_todos = Todo.objects.filter(completed=True).count()
        pending_todos = total_todos - completed_todos
        
        # 分類統計
        categories_stats = Category.objects.annotate(
            total_todos=Count('todos'),
            completed_todos=Count('todos', filter=Q(todos__completed=True))
        ).values('name', 'total_todos', 'completed_todos')
        
        # 最近7天的每日任務統計
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        daily_stats = (
            Todo.objects
            .filter(created_at__gte=seven_days_ago)
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(
                total=Count('id'),
                completed=Count('id', filter=Q(completed=True))
            )
            .order_by('day')
        )

        # 每小時任務創建趨勢
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        hourly_stats = (
            Todo.objects
            .filter(created_at__gte=today)
            .annotate(hour=TruncHour('created_at'))
            .values('hour')
            .annotate(count=Count('id'))
            .order_by('hour')
        )

        # 完成率統計
        completion_rate = (completed_todos / total_todos * 100) if total_todos > 0 else 0
        
        # 準備圖表數據
        daily_labels = [stat['day'].strftime('%Y-%m-%d') for stat in daily_stats]
        daily_total = [stat['total'] for stat in daily_stats]
        daily_completed = [stat['completed'] for stat in daily_stats]
        
        hourly_labels = [stat['hour'].strftime('%H:00') for stat in hourly_stats]
        hourly_data = [stat['count'] for stat in hourly_stats]
        
        context = {
            'title': 'Todo 儀表板',
            'total_todos': total_todos,
            'completed_todos': completed_todos,
            'pending_todos': pending_todos,
            'completion_rate': round(completion_rate, 2),
            'categories_stats': list(categories_stats),
            'daily_labels': daily_labels,
            'daily_total': daily_total,
            'daily_completed': daily_completed,
            'hourly_labels': hourly_labels,
            'hourly_data': hourly_data,
            'opts': self.model._meta,
        }
        
        return TemplateResponse(request, 'admin/todo_dashboard.html', context)
