from django.contrib import admin
from .models import Project, Transaction
from django.utils.html import format_html

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag', 'description')
    search_fields = ('name',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'project', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_id', 'invoice_id')
    readonly_fields = ('raw_data',)