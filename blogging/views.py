from django.shortcuts import render, HttpResponse, redirect
from blogging.models import Post,BlogComment
from django.contrib import messages
from blogging.templatetags import extras
import math

# Create your views here.
def bloggingHome(request):
    no_of_posts = 3
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    '''
    1 : 0-3
    2 : 3-6
    3 : 6-9 

    1 : 0 - 0 + no_of_posts
    2 : no_of_posts to no_of_posts + no_of_posts
    3 : no_of_posts + no_of_posts to no_of_posts + no_of_posts + no_of_posts

   (page_no-1)*no_of_posts to page_no*no_of_posts
    '''
    allPosts = Post.objects.all()
    length = len(allPosts)
    # print(length)
    allPosts = allPosts[(page-1)*no_of_posts : page*no_of_posts]
    if page>1:
        prev = page - 1
    else:
        prev = None

    if page<math.ceil(length/no_of_posts):
        nxt = page + 1
    else:
        nxt = None
    context = {'allPosts': allPosts, 'prev': prev, 'nxt': nxt}
    return render(request, 'blogging/blog_home.html', context)
    # return HttpResponse('This is blog home. All blog post will be kept here.')


def bloggingPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    print(replyDict)
    context = {'post' : post, 'comments': comments, 'user':request.user, 'replyDict':replyDict}
    # return HttpResponse(f'This is blogPost: {slug}')
    return render(request, 'blogging/blogpost.html', context)  




def postComment(request):
    if request.method=='POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            messages.success(request, "Your comment has been posted successfully")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            messages.success(request, "Your reply has been posted successfully")

        comment.save()

    return redirect(f"/blogging/{post.slug}")
