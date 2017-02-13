from django.contrib import admin
from forum.models import Post, Topic
from django.shortcuts import render
from django.template import loader

class PostAdmin(admin.ModelAdmin):
    list_display = ('Author', 'topic', 'Creation_Data', 'id')

    def topic(self, obj):
        return obj.Topic.admin_url()

    topic.allow_tags = True


class TopicAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Creator', 'Creation_Data', 'post_count' ,'id')
    readonly_fields = ('posts',)
    extra_field = ('posts',)


    def post_count(self, obj):
        return obj.post_set.count()

    def posts(self, obj):
        return loader.get_template('post_list_admin.html').render({'posts': obj.post_set.all()})


    posts.allow_tags = True

admin.site.register(Post, PostAdmin)
admin.site.register(Topic,TopicAdmin)
