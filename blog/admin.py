from django.contrib import admin
from .models import Post, Tag, Image, Comment, User
from .models.like.models import Like


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'updated_at']
    list_filter = ['status', 'author', 'updated_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'updated_at'
    ordering = ['status', 'updated_at']
    filter_horizontal = (
        "tags",
    )
    inlines = [
        ImageInline
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
