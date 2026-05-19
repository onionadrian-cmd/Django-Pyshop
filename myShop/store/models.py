from django.db import models
from django.urls import reverse
from colorfield.fields import ColorField

class WebsiteCustomization(models.Model):
    primary_color = ColorField(default='#0066cc')
    secondary_color = ColorField(default='#ff9900')
    accent_color = ColorField(default='#00cc66')

    background_type = models.CharField(
        max_length=10,
        choices=[('color', 'Color'), ('gradient', 'Gradient'), ('image', 'Image')],
        default='color'
    )
    background_color = ColorField(default='#ffffff')
    background_gradient = models.CharField(
        max_length=255,
        default='linear-gradient(135deg, #ffffff, #f5f5f5)',
        help_text='CSS gradient format, e.g., linear-gradient(135deg, #fff, #f5f5f5)'
    )
    background_image = models.ImageField(upload_to='backgrounds/', null=True, blank=True)

    text_color = ColorField(default='#333333')
    heading_color = ColorField(default='#000000')

    button_color = ColorField(default='#0066cc')
    button_text_color = ColorField(default='#ffffff')
    button_hover_color = ColorField(default='#0052a3')
    button_hover_text_color = ColorField(default='#ffffff')

    link_color = ColorField(default='#0066cc')
    link_hover_color = ColorField(default='#0052a3')

    header_background = ColorField(default='#ffffff')
    footer_background = ColorField(default='#333333')
    footer_text_color = ColorField(default='#ffffff')

    class Meta:
        verbose_name_plural = "Website Customization"

    def __str__(self):
        return "Website Customization Settings"

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or f"Banner {self.id}"

    class Meta:
        ordering = ['-id']

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    product_description = models.TextField(blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_stock = models.IntegerField()
    images = models.ImageField(upload_to='product_images/',)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name