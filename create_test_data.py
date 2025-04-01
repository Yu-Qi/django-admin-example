import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoapi.settings')
django.setup()

from todos.models import Category, Todo

# 創建分類
categories_data = [
    {'name': '工作', 'description': '工作相關任務'},
    {'name': '學習', 'description': '學習和進修相關'},
    {'name': '生活', 'description': '日常生活事務'},
    {'name': '健康', 'description': '運動和健康相關'},
    {'name': '娛樂', 'description': '休閒娛樂活動'}
]

# 清除現有數據
print('清除現有數據...')
Todo.objects.all().delete()
Category.objects.all().delete()

# 創建分類
print('創建分類...')
categories = []
for cat_data in categories_data:
    category = Category.objects.create(**cat_data)
    categories.append(category)

# 待辦事項範本
todos_templates = {
    '工作': [
        ('完成季度報告', 'https://example.com/report', '準備第一季度的工作報告'),
        ('客戶會議', 'https://meet.google.com', '與重要客戶進行產品討論'),
        ('專案規劃', 'https://trello.com', '規劃下個月的專案進度'),
        ('團隊會議', 'https://zoom.us', '週期性團隊同步會議'),
        ('代碼審查', 'https://github.com', '審查團隊成員的代碼提交')
    ],
    '學習': [
        ('Python 課程', 'https://coursera.org', '完成 Python 進階課程'),
        ('英語學習', 'https://duolingo.com', '每日英語練習'),
        ('技術文章', 'https://medium.com', '閱讀技術文章提升知識'),
        ('線上研討會', 'https://webinar.com', '參加技術研討會'),
        ('實作練習', 'https://leetcode.com', '算法練習')
    ],
    '生活': [
        ('購物清單', 'https://shopping.com', '採購日常用品'),
        ('繳費提醒', 'https://bank.com', '繳交水電費'),
        ('整理房間', '', '週末大掃除'),
        ('修理物品', '', '修理損壞的家具'),
        ('預約維修', 'https://repair.com', '預約冷氣維修')
    ],
    '健康': [
        ('晨跑', 'https://nike.com', '完成 5 公里晨跑'),
        ('健身', 'https://gym.com', '重訓課程'),
        ('營養規劃', 'https://diet.com', '規劃健康飲食'),
        ('睡眠追蹤', 'https://sleep.com', '記錄睡眠品質'),
        ('喝水提醒', '', '確保每日飲水量')
    ],
    '娛樂': [
        ('看電影', 'https://netflix.com', '觀看最新電影'),
        ('讀書', 'https://goodreads.com', '閱讀小說'),
        ('遊戲時間', 'https://steam.com', '玩遊戲放鬆心情'),
        ('戶外活動', 'https://hiking.com', '週末郊遊計畫'),
        ('音樂會', 'https://concert.com', '預約音樂會門票')
    ]
}

# 創建待辦事項
print('創建待辦事項...')
now = datetime.now()
for category in categories:
    templates = todos_templates[category.name]
    # 為每個分類創建 15-20 個待辦事項
    for _ in range(random.randint(15, 20)):
        template = random.choice(templates)
        created_date = now - timedelta(days=random.randint(0, 14))
        completed = random.choice([True, False])
        if completed:
            created_date = created_date - timedelta(days=random.randint(1, 7))
        
        Todo.objects.create(
            title=template[0],
            url=template[1],
            description=template[2],
            category=category,
            completed=completed,
            created_at=created_date
        )

print('完成創建測試數據！') 