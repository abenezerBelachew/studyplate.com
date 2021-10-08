from django.contrib import admin


from .models import Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('subject', 'content', 'author', 
    'created_at',)
    list_filter = ('author', 'course',)
    search_fields = ('subject', 'content',)
    inlines = [CommentInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at',)
    list_filter = ('content', 'author',)
    