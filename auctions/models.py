from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return f"{self.name}"

class Auction(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
	title = models.CharField(max_length=64)
	description = models.TextField()
	start = models.DecimalField(null=True, max_digits=8, decimal_places=2, default=None)
	startbid = models.DecimalField(max_digits=8, decimal_places=2, null=True)
	image = models.FileField(upload_to="gallery")
	category = models.ManyToManyField(Category, default="No category", related_name="auctions")
	active = models.BooleanField(default=True)
	buyer = models.CharField(max_length=64, default="Nobody")
	
	def __str__(self):
		return f"{self.title}({self.description}):{self.startbid}"

class Bid(models.Model):
	price = models.DecimalField(max_digits=8, decimal_places=2)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
	item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")

	def __str__(self):
		return f"{self.price} for {self.item} by {self.user}"

class Comment(models.Model):
	texty = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
	item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")

	def __str__(self):
		return f"{self.texty}"

class Watchlist(models.Model):
	user = models.CharField(max_length=64)
	item = models.IntegerField()