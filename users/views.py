from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

#coreySchafer
def register(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        # Si la requête est une méthode POST, cela signifie que le formulaire a été soumis
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            # Si le formulaire est valide, enregistrez l'utilisateur
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        # Si la requête n'est pas une méthode POST, affichez simplement le formulaire vide
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# coreySchafer
@login_required
def profile(request):
    """
    View for user profile.
    """
    if request.method == 'POST':
        # Si la requête est une méthode POST, cela signifie que le formulaire a été soumis
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            # Si les formulaires sont valides, sauvegardez les modifications
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        # Si la requête n'est pas une méthode POST, affichez simplement les formulaires remplis avec les données actuelles
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
