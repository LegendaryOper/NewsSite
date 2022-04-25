from django.shortcuts import render, get_object_or_404, redirect
from news.models import News, NewsComment
from news.forms import NewsForm, CommentForm, RegistrationForm, UserLoginForm
from django.views.generic import ListView, CreateView
from django.db.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import MyMixin
from django.contrib import messages
from django.contrib.auth import login, logout


# Create your views here.
class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    mixin_prop = 'Привет'
    paginate_by = 3

    def get_queryset(self):
        return News.objects.all().select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['mixin'] = self.get_prop()
        return context


class Categories(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id']).select_related('category')

# class get_post(CreateView):
#     model=News
#     template_name = 'news/post.html'
#     context_object_name = 'post'
#     def get_context_data(self, **kwargs):
#         context=super(get_post, self).get_context_data(**kwargs)
#         context['comments']=NewsComment.objects.filter(news_id=context['pk'])
#         return context


#
# def index(request):
#     news=News.objects.all()
#     context={'news':news,'title':'Cписок новостей',}
#     return render(request,'news/index.html',context)

# def get_category(request,category_id):
#     news=News.objects.filter(category_id=category_id)
#     category=get_object_or_404(Category,pk=category_id)
#     context={'news':news,'category':category,}
#     return render(request,'news/category.html',context)

def get_post(request, pk):
    post = get_object_or_404(News, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        comments = NewsComment.objects.filter(news_id=pk)
        _mutable = form.data._mutable
        form.data._mutable = True
        form.data.update({'author': request.user.username, 'mail': request.user.email})
        form.data._mutable = _mutable
        if form.is_valid():
            comment = form.save()
            comment.news_id = post
            comment.save()
            return redirect(post)
    else:
        post.views = F('views')+1
        post.save(update_fields=['views'])
        form = CommentForm()
        comments = NewsComment.objects.filter(news_id=pk)
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'news/post.html', context)

# def new_post(request):
#     if request.method=='POST':
#         form=NewsForm(request.POST)
#         if form.is_valid():
#            # print(form.cleaned_data)
#            # news=News.objects.create(**form.cleaned_data)
#             news=form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/new_post.html',{'form': form})


class new_post(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/new_post.html'
    raise_exception = True


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно')
        else:
            messages.error(request, 'Упс... Зарегистрироваться не удалось')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'news/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Поздравляем! Вы успешно вошли в учетную запись')
            return redirect('home')
        else:
            messages.error(request, 'Упс... Войти не удалось')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'news/login.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из учетной записи')
    return redirect('home')
