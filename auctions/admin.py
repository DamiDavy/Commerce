from django.contrib import admin

from .models import User, Category, Auction, Bid, Comment, Watchlist

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Watchlist)

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'startbid', 'active', 'buyer')

class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'price')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'texty')

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)