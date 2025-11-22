from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UserProfile
from .forms import UserForm, UserProfileForm

class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('library:book_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ви успішно увійшли в систему!')
        return super().form_valid(form)

class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('library:book_list')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Ви вийшли з системи.')
        return super().dispatch(request, *args, **kwargs)
    
class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('library:book_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Реєстрація пройшла успішно! Ласкаво просимо!')
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile_edit.html'
    form_class = UserForm
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = UserProfileForm(self.request.POST, self.request.FILES, instance=self.object.profile)
        else:
            context['profile_form'] = UserProfileForm(instance=self.object.profile)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        
        if profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(self.request, 'Профіль успішно оновлено!')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))