from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Gig, Profile, Purchase, Review
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .forms import GigForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.

def index(request):
    gigs = Gig.objects.filter(status=True)
    context = {
        'gigs': gigs
    }
    return render(request, 'index.html', context)

def gig_detail(request, gig_id):

  if request.method == 'POST' and \
    not request.user.is_anonymous and \
    Purchase.objects.filter(gig_id=gig_id, buyer=request.user).count() > 0 and \
    'content' in request.POST and \
    request.POST['content'].strip() != '':
    Review.objects.create(content=request.POST['content'], gig_id= gig_id, user=request.user)

  try:
    gig = get_object_or_404(Gig, pk=gig_id)
  except Gig.DoesNotExist:
      return redirect('index')

  if request.user.is_anonymous or \
    Purchase.objects.filter(gig=gig, buyer=request.user).count() == 0 or \
    Review.objects.filter(gig=gig, user=request.user).count() > 0:
    show_post_review = False
  else:
    show_post_review = Purchase.objects.filter(gig=gig, buyer=request.user).count() > 0

  reviews = Review.objects.filter(gig=gig)

  context = {
      'gig': gig,
      'show_post_review': show_post_review,
      'reviews': reviews
  }

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

  return render(request, 'gig_detail.html', context)

def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render(request, 'register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('index')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
    return redirect('index')


def profil(request, username):
  if request.method == 'POST':
    profile = Profile.objects.get(user=request.user)
    profile.about = request.POST['about']
    profile.slogan = request.POST['slogan']
    profile.save()
  else:
    try:
      profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
      return redirect('index')
  gigs = Gig.objects.filter(user=profile.user, status=True)

  context = {
    'profile': profile,
    'gigs': gigs
  }
  return render(request, 'profil.html', context)

@login_required(login_url="login")
def my_gig(request):
  gigs = Gig.objects.filter(user=request.user)

  context = {
    'gigs': gigs
  }
  return render(request, 'my_gig.html', context)

def create_gig(request):
  if request.method == 'POST':
    gig_form = GigForm(request.POST, request.FILES)
    if gig_form.is_valid():
        gig = gig_form.save(commit=False)
        gig.user = request.user
        gig.save()
        return redirect('my_gig')
    else:
        messages.error(request, 'Verifier vos entrés')
    gig_form = GigForm()
  return render(request, 'create_gig.html')


@login_required(login_url="login")
def edit_gig(request, gig_id):
    try:
        gig = get_object_or_404(Gig, pk=gig_id)
        error = ''
        if request.method == 'POST':
            gig_form = GigForm(request.POST, request.FILES, instance=gig)
            if gig_form.is_valid():
                gig.save()
                return redirect('my_gig')
            else:
                messages.error(request, 'Les données sont invalides')
        context = {
          'gig': gig
        }
        return render(request, 'edit_gig.html', context)
    except Gig.DoesNotExist:
        return redirect('index')

@login_required(login_url="login")
def mes_ventes(request):
  purchases = Purchase.objects.filter(gig__user=request.user)
  context = {
    'purchases': purchases
  }
  return render(request, 'mes_ventes.html', context)

@login_required(login_url="login")
def mes_achats(request):
  purchases = Purchase.objects.filter(buyer=request.user)

  context = {
    'purchases': purchases
  }
  return render(request, 'mes_achats.html', context)

def category(request, link):
    categories = {
        "graphics-design": "GD",
        "digital-marketing": "DM",
        "video-animation": "VA",
        "music-audio": "MA",
        "programming-tech": "PT"
    }
    try:
        gigs = Gig.objects.filter(category=categories[link])
        context = {
          'gigs': gigs
        }
        return render(request, 'index.html', context)
    except KeyError:
        return redirect('index')

def search(request):
  gigs = Gig.objects.filter(title__contains=request.GET['title'])

  context = {
    'gigs': gigs
  }
  return render (request, 'index.html', context)

@login_required(login_url="/")
def create_purchase(request):
    if request.method == 'POST':
        try:
            gig = Gig.objects.get(id = request.POST['gig_id'])
        except Gig.DoesNotExist:
            return redirect('index')

        charge = stripe.Charge.create(
            amount= gig.price,
            currency='XOF',
            description= gig.title,
            source=request.POST['stripeToken']
        )

        if charge.is_success:
            Purchase.objects.create(gig=gig, buyer=request.user)
    return redirect('index')