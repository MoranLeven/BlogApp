from django.urls import path
from .views import CreateBlog, HomeBlog, UpdateBlog, LookBlog, ReplyBlog
from django.conf.urls.static  import static
from django.conf import settings
urlpatterns = [
    path("create",CreateBlog.as_view(),name="create_blog"),
    path("update/<uuid:uuid>",UpdateBlog.as_view(),name="update_blog"),
    path("blog/<uuid:uuid>",LookBlog.as_view(),name="blog" ),
    path("addReply",ReplyBlog.as_view(),name="addReply"),
    path("getReply",ReplyBlog.as_view(),name="getReply"),
    path("deleteReply",ReplyBlog.as_view(),name="deleteReply"),
    path("updateReply",ReplyBlog.as_view(),name="updateReply"),
    path("",HomeBlog.as_view(),name="home")
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)