from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, FAQ, Event, Feedback
from .forms import PostForm, FAQForm, EventForm
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

def home(request):
    lang = request.GET.get('lang', 'en')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            Feedback.objects.create(name=name, email=email, message=message)
            return redirect('home')
            
    all_posts = Post.objects.filter(language=lang).order_by('-created_at')

    paginator = Paginator(all_posts, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        posts_data = []
        for post in page_obj:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'content_snippet': post.content[:100],
                'post_type': post.post_type,
                'image_url': post.image.url if post.image else None,
                'video_url': post.video.url if post.video else None,
            })
        return JsonResponse({'posts': posts_data})
    
    event = Event.objects.filter(show=True).order_by('date').first()
    context = {
        'posts': page_obj,
        'event': event,
        'lang': lang,
    }
    return render(request, 'core/home.html', context)


def posts_list(request):
    lang = request.GET.get('lang', 'en')
    all_posts = Post.objects.filter(language=lang).order_by('-created_at')

    paginator = Paginator(all_posts, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        posts_data = []
        for post in page_obj:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'content_snippet': post.content[:100],
                'post_type': post.post_type,
                'image_url': post.image.url if post.image else None,
                'video_url': post.video.url if post.video else None,
            })
        return JsonResponse({'posts': posts_data})
    
    context = {
        'posts': page_obj,
        'lang': lang,
    }
    return render(request, 'core/posts_list.html', context)


def get_post_content_ajax(request, pk):
    post = get_object_or_404(Post, pk=pk)
    data = {
        'title': post.title,
        'content': post.content,
        'post_type': post.post_type,
        'image_url': post.image.url if post.image else None,
        'video_url': post.video.url if post.video else None,
    }
    return JsonResponse(data)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts_list')
    else:
        form = PostForm()
    return render(request, 'core/post_form.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'core/post_form.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('posts_list')
    return render(request, 'core/post_confirm_delete.html', {'post': post})


def events_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'core/events_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'core/event_detail.html', {'event': event})


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('events_list')
    else:
        form = EventForm()
    return render(request, 'core/event_form.html', {'form': form})


def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'core/event_form.html', {'form': form})


def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('events_list')
    return render(request, 'core/event_confirm_delete.html', {'event': event})


def faqs_list(request):
    lang = request.GET.get('lang', 'en')
    faqs = FAQ.objects.filter(language=lang).order_by('id')
    context = {
        'faqs': faqs,
        'lang': lang,
    }
    return render(request, 'core/faqs_list.html', context)


def create_faq(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faqs_list')
    else:
        form = FAQForm()
    return render(request, 'core/faq_form.html', {'form': form})


def edit_faq(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect('faqs_list')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'core/faq_form.html', {'form': form})


def delete_faq(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        return redirect('faqs_list')
    return render(request, 'core/faq_confirm_delete.html', {'faq': faq})

def dashboard(request):
    return render(request, 'core/dashboard.html')
