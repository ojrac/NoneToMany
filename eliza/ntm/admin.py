from django.contrib import admin

from ntm.models import Conversation, Exchange

class ExchangeInline(admin.TabularInline):
    model = Exchange
    extra = 0

class ConversationAdmin(admin.ModelAdmin):
    inlines = [ExchangeInline]
    list_display = ('start_time', 'num_exchanges')

admin.site.register(Conversation, ConversationAdmin)


