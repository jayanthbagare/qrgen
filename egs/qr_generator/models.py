from django.db import models
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
from PIL import Image
import requests
from django.conf import settings
from django.conf.urls.static import static
import os

class QRCode(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    url = models.URLField()
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        logo_link = os.path.join(settings.MEDIA_ROOT,"hakki.png")
        logo = Image.open(logo_link)

        basewidth = 100
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth,hsize))
        
        # Generate QR code
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(self.url)
        qr.make()
        
        # Create image
        img = qr.make_image()
        pos=((img.size[0]-logo.size[0])//2,(img.size[1]-logo.size[1])//2)
        img.paste(logo,pos)

        # Save QR code image
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr_{self.id}.png'
        
        # Save to model
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id
