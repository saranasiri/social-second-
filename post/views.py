from django.shortcuts import render, get_object_or_404, redirect
from .models import post, comment ,vote
from .form import AddPostForm, Editepostform, Addcommentform,Addreplyform
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required


def all_post(request):
    posts = post.objects.all()
    return render(request, 'post/all.html', {'posts': posts})


def post_detail(request, year, month, day, slug):
    posts = get_object_or_404(post, created__year=year, created__month=month, created__day=day, slug=slug)
    comments = comment.objects.filter(post=posts, is_reply=False)
    reply_form=Addreplyform()
    can_like = False
    if request.user.is_authenticated:
        if posts.user_can_like(request.user):
            can_like = True
    if request.method == 'POST':
        form = Addcommentform(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = posts
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'your comment is sended', 'success')

    else:
        form = Addcommentform()
    return render(request, 'post/post_detail.html', {'post': posts, 'comments': comments, 'form': form , 'reply_form': reply_form ,'can_like':can_like})


@login_required
def add_post(request, user_id):
    if request.user.id == user_id:
        if request.method == 'POST':
            form = AddPostForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.slug = slugify(form.cleaned_data['body'][:30])
                new_post.save()
                messages.success(request, 'your post submited', 'success')
                return redirect('account:dashboard', user_id)
        else:
            form = AddPostForm()
            return render(request, 'post/add_post.html', {'form': form})
    else:
        return redirect('posts:all_posts')


@login_required
def post_delete(request, user_id, post_id):
    if user_id == request.user.id:
        post.objects.filter(id=post_id).delete()
        messages.success(request, 'your post delete successfully', 'success')
        return redirect('account:dashboard', user_id)
    else:
        return redirect('post:all_posts')


@login_required
def edit_post(request, user_id, post_id):
    if request.user.id == user_id:
        Post = get_object_or_404(post, id=post_id)
        if request.method == 'POST':
            form = Editepostform(request.POST, instance=Post)
            if form.is_valid():
                new_edit = form.save(commit=False)
                new_edit = request.user
                new_edit.slug = slugify(form.cleaned_data['body'][:30])
                new_edit.save()
                messages.success(request, 'your post changed', 'success')
                return redirect('account:dashboard', user_id)


        else:
            form = Editepostform(instance=Post)
            return render(request, 'post/edit_post.html', {'form': form})
    else:
        return redirect('post:all_posts')


@login_required
def Add_reply(request,post_id,comment_id):
   posts=get_object_or_404(post,id = post_id)
   comments=get_object_or_404(comment,id=comment_id)
   if request.method=='POST':
       form=Addreplyform(request.POST)
       if form.is_valid():
            reply= form.save(commit=False)
            reply.user=request.user
            reply.post=posts
            reply.reply = comments
            reply.is_reply = True
            reply.save()
            messages.success(request,'your reply submited','success')
   return redirect('post:post_detail',posts.created.year , posts.created.month , posts.created.day, posts.slug)



@login_required
def like_post(request , post_id):
    Post = get_object_or_404(post , id = post_id)
    like = vote(post=Post , user=request.user)
    like.save()
    messages.success(request, 'you liked successfully', 'success')
    return redirect('post:post_detail',Post.created.year,Post.created.month,Post.created.day,Post.slug)



