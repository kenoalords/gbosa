from django.contrib import admin
from app.models import Answer, Post, View, Upvote, Comment, Region, PsuedoUser

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = { "slug": ('title',) }

admin.site.register(Answer)
admin.site.register(View)
admin.site.register(Upvote)
admin.site.register(Comment)
admin.site.register(Region)
admin.site.register(PsuedoUser)
admin.site.register(Post, PostAdmin)
