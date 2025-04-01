from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Todo, Category
from .serializers import TodoSerializer, CategorySerializer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True)
    def todos(self, request, pk=None):
        category = self.get_object()
        todos = category.todos.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        queryset = Todo.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

    @action(detail=False)
    def categories_stats(self, request):
        stats = Category.objects.annotate(
            total_todos=Count('todos'),
            completed_todos=Count('todos', filter=models.Q(todos__completed=True))
        ).values('id', 'name', 'total_todos', 'completed_todos')
        return Response(stats)
