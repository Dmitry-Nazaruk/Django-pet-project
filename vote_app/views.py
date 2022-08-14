from django.contrib import messages

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import Q
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, FormView, DetailView

from vote_app.forms import PostForm, RegForm, CommentForm, UpdateProfileForm
from vote_app.models import Posts, Comments, Customuser



class Main_html(View):

    def get(self, request):
        posts = Posts.objects.values_list('body', 'title', 'ratings', 'username').order_by('-ratings')
        first_last_name = Customuser.objects.all()
        paginator = Paginator(posts, 10)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'main.html', {'page_obj': page_obj})

    def post(self, request):
        posts = Posts.objects.values_list('body', 'title', 'ratings', 'username')
        posts = Posts.objects.filter(Q(title__icontains=request.POST['search_title']) | Q(body__icontains=request.POST['search_title']))
        paginator = Paginator(posts, 10)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'main.html', {'page_obj_search': page_obj})



class RegisterFormView(FormView):
    form_class = RegForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))


class Create_Post(View):
    template_name = 'create_post.html'

    def get(self, request):
        form = PostForm()
        return render(request,'create_post.html', context={'post_form': form})

    def post(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                user = request.user
                form = form.save(commit=False)
                form.username = str(user)
                form.save()
        return redirect('/')


class All_post_main(View):

    def get(self, request):
        posts = Posts.objects.values_list('body', 'title', 'ratings', 'username')
        user = request.user
        posts = Posts.objects.filter(username=user)
        return render(request, 'posts_user.html', context={'posts': posts, 'post_form': PostForm})

class PostDetail(DetailView):
    model = Posts
    template_name = 'post_detail.html'
    context_object_name = 'context'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['comment'] = Comments.objects.filter(post_id=self.kwargs['pk'])
        return context




class Create_comment(View):
    template_name = 'create_comment.html'

    def get(self, request, pk):
        form = CommentForm()
        return render(request, 'create_comment.html', context={'comment_form': form })

    def post(self, request, pk):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                user = request.user
                form = form.save(commit=False)
                form.post_id = Posts.objects.get(id=pk)
                form.save()
        return redirect('/')


class Profile(View):
    template_name = 'profile.html'

    def get(self, request):
        form = Customuser()
        return render(request,'profile.html', context={'post_form': form})

class Change_User(View):
    template_name = 'change_profile.html'

    def get(self, request):
        form = UpdateProfileForm()
        return render(request,'change_profile.html', context={'form': form})

    def post(self, request):
        if request.method == 'POST':
            profile_form = UpdateProfileForm(request.POST)
            user = request.user
            change_user = Customuser.objects.filter(user_name=user).update(email=request.POST.get('email'),
                                                                           first_name=request.POST.get('first_name'),
                                                                           last_name=request.POST.get('last_name'),
                                                                           date_birth=request.POST.get('date_birth'),
                                                                           city=request.POST.get('city'))
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile is updated successfully')
                return redirect('/profile')
        else:
            profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'change_profile.html', {'profile_form': profile_form})