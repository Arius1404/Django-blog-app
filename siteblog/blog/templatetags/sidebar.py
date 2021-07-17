from django import template
from django.db.models import Count
from blog.models import Tag, Post

register = template.Library()


@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular_posts(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt][:5]
    return {"posts": posts, "comments": "#comments"}


@register.inclusion_tag('blog/tag_cloud.html')
def get_tag_cloud():
    tags = Tag.objects.annotate(cnt=Count('posts')).filter(cnt__gt=0)
    return {"tags": tags}
