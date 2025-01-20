# qr_generator/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import QRCode

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'created_at', 'qr_code_preview', 'download_link')
    search_fields = ('id', 'url')
    readonly_fields = ('created_at', 'qr_code_preview')
    fields=['id','url']
    
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" style="width: 150px;" />', obj.qr_code.url)
        return "No QR Code"
    qr_code_preview.short_description = 'QR Code Preview'
    
    def download_link(self, obj):
        if obj.qr_code:
            return format_html('<a href="{}" download>Download QR Code</a>', obj.qr_code.url)
        return "No QR Code"
    download_link.short_description = 'Download'
