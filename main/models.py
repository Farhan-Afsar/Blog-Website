from django.db import models
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    excerpt = models.TextField(max_length=500, blank=True, help_text="A short summary of the post")
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, help_text="Upload an image for this blog post")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_related_posts(self):
        """Get other posts excluding the current one"""
        return Post.objects.filter(status='published').exclude(id=self.id).order_by('-created_at')[:3]
    
    @property
    def has_image(self):
        """Check if the post has an image"""
        return bool(self.image)
    
    @property
    def get_excerpt(self):
        """Get excerpt or generate one from content"""
        if self.excerpt:
            return self.excerpt
        return self.content[:200] + "..." if len(self.content) > 200 else self.content
