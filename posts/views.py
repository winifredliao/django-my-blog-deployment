import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm

class StartingPageView(ListView):
    template_name = "posts/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class AllPostsView(ListView):
    template_name = "posts/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

class SinglePostView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        post_content_html = markdown.markdown(
            post.content, extensions=["fenced_code", "codehilite"]
        )
        context = {
            "post": post,
            "post_content_html": post_content_html,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "posts/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        post_content_html = markdown.markdown(
            post.content, extensions=["fenced_code", "codehilite"]
        )

        if comment_form.is_valid():
          comment = comment_form.save(commit=False)
          comment.post = post
          comment.save()
          
          return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_content_html": post_content_html,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "posts/post-detail.html", context)