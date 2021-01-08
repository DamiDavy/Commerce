from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import User, Category, Auction, Bid, Comment, Watchlist
from .forms import AuctionForm
import os


def index(request):
    auctions = Auction.objects.filter(active=True)
    nonactive = Auction.objects.filter(active=False)
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "nonactive": nonactive
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def new(request):
    categories = Category.objects.all()
    users = User.objects.all()
    for user in users:
        if user.is_authenticated:
            idd = user.id
            owner = User.objects.get(pk=idd)
    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start = form.cleaned_data["startbid"]
            image = request.FILES['file']
            auction = Auction(user=owner, title=title, description=description, start=start, image=image)
            auction.save()
            listiks = request.POST.getlist('category')
            for listik in listiks:
                category_id = int(listik)
                category = Category.objects.get(pk=category_id)
                auction.category.add(category)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new.html", {
                "form": form
            })
    else:
        return render(request, "auctions/new.html", {
            "form": AuctionForm(),
            "categories": categories
    })


def listing(request, num):
    listing = Auction.objects.get(pk=num)
    group = listing.category.all()
    users = User.objects.all()
    for user in users:
        if user.is_authenticated:
            name = user.username
            author = User.objects.get(pk=user.id)
            if request.method == "POST":
                comment = request.POST["comment"]
                create = Comment(texty=comment, user=author, item=listing)
                create.save()
                return HttpResponseRedirect(reverse("listing", args=(num,)))
            else:
                comments = Comment.objects.filter(item=listing)
                added = Watchlist.objects.filter(user=name, item=num) 
                return render(request, "auctions/listing.html", {
                    "added": added,
                    "listing": listing,
                    "group": group,
                    "comments": comments
                    })

@login_required
def wish(request, num):
    listing = Auction.objects.get(pk=num)
    group = listing.category.all()
    n = listing.user.id
    users = User.objects.exclude(pk=n)
    for user in users:
        if user.is_authenticated:
            name = user.username
            wish = Watchlist.objects.filter(user=name, item=num)
            if wish:
                wish.delete()
                return HttpResponseRedirect(reverse("listing", args=(num,)))
            else:
                wish = Watchlist(user=name, item=num)
                wish.save()
                return HttpResponseRedirect(reverse("listing", args=(num,)))

@login_required
def bid(request, num):
    if request.method == "POST":
        listing = Auction.objects.get(pk=num)
        group = listing.category.all()
        n = listing.user.id
        users = User.objects.exclude(pk=n)
        for user in users:
            if user.is_authenticated:
                name = user.username
                bids = Bid.objects.filter(item=listing)
                bid = bids.order_by('-price').first()
                mybid = float(request.POST["bid"])
                if bid is None:
                    maxprice = listing.start
                else:
                    maxprice = float(bid.price)
                    if maxprice > mybid:
                        listing.startbid = maxprice
                        added = Watchlist.objects.filter(user=name, item=num)
                        comments = Comment.objects.filter(item=listing)
                        return render(request, "auctions/listing.html", {
                            "added": added,
                            "listing": listing,
                            "group": group,
                            "comments": comments,
                            "mes": "Your bid should be greater than previous"
                            })
                    else:
                        listing.startbid = mybid
                buyer = User.objects.get(pk=user.id)
                ist = Bid(price=mybid, user=buyer, item=listing)
                ist.save()
                listing.buyer = user.username
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(num,)))

@login_required
def close(request, num):
    listing = Auction.objects.get(pk=num)
    listing.active = False
    listing.save()
    watch = Watchlist.objects.filter(item=num)
    for i in watch:
        i.delete()
    return HttpResponseRedirect(reverse("listing", args=(num,)))

@login_required
def watchlist(request, name):
    here = Watchlist.objects.filter(user=name)
    auctions = []
    for i in here:
        j = i.item
        auction = Auction.objects.get(pk=j)
        auctions.append(auction)
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions,
        })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
        })

def category(request, title):
    category = Category.objects.get(name=title)
    au = category.auctions.all()
    auctions = []
    for a in au:
        if a.active == True:
            auctions.append(a)
    return render(request, "auctions/category.html", {
        "category": category,
        "auctions": auctions
        })
