from django.contrib import admin
from .models import Author, BlogPost, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('author', 'content', 'created_at')
    ordering = ('-created_at',)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('title', 'content')
    inlines = [CommentInline]

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__user__username')
    readonly_fields = ('created_at',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
