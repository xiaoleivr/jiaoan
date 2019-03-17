from django.contrib import admin
from .models import Profile,Contact,Category,Post,Comment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user_from','user_to')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status', 'created',)
    # 右侧过滤列表侧边栏
    list_filter = ('status', 'created', 'publish',)
    # 用于1对多，可以通过id查询
    raw_id_fields = ('category',)
    # 横向筛选类别
    date_hierarchy = 'publish'
    # 显示排序小三角
    ordering = ('status', 'publish', 'created',)

#
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user',)