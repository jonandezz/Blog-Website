from django.shortcuts import render, redirect
from .models import PostModel 
from .forms import PostModelForm,PostUpdateForm,CommentForm
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def index_home(request, *args, **kwargs):
    posts = PostModel.objects.all()
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
           instance = form.save(commit=False)
           instance.author = request.user
           instance.save()
           return redirect('home')
    else:        
        form = PostModelForm   
    context = {
        'posts': posts,
        'form': form
    }
    posts = PostModel.objects.all()
    form = PostModelForm   
    return render(request,'blog/index.html', context)  

@login_required
def post_detail(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method =='POST':
         c_form = CommentForm(request.POST)
         if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('post_detail', pk=post.id)
    else:
        c_form = CommentForm()

    context={
        'post':post,
        'c_form': c_form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_edit(request, pk):
    post=PostModel.objects.get(id=pk)
    if request.method=='POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save() 
            return redirect('post_detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context={
        'post':post,
        'form':form,
    }
    return render(request, 'blog/post_edit.html', context)
    
@login_required
def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method=='POST':
        post.delete()
        return redirect('home')
    context={
        'post':post,
    }
    return render(request, 'blog/post_delete.html', context)
