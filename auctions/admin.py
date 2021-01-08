from django.contrib import admin

from .models import User, Category, Auction, Bid, Comment, Watchlist

admin.site.register(User)
admin.site.register(Category)
#admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'startbid', 'active', 'buyer')

admin.site.register(Auction, AuctionAdmin)