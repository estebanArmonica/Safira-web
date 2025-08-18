from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .choices import CATEGORY_CHOICES

# Create your models here.
class BlogPost(models.Model):
    id_blog = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    featured_image = models.ImageField(upload_to='blog/')
    excerpt = models.TextField()
    content = models.TextField()
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'blog_post'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
            # nos aseguramos que el slug sea único
            original_slug = self.slug
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug':self.slug})
    
    def __str__(self):
        return f'{self.id_blog} - {self.title} - {self.created_at} - {self.updated_at}'
    
    
class fotoBlog(models.Model):
    id_foto_blog = models.AutoField(primary_key=True)
    url_foto_blog = models.CharField(max_length=255)
    nombre_foto_blog = models.CharField(max_length=255)
    tipo = models.CharField(max_length=25)
    id_blog = models.ForeignKey(BlogPost, models.DO_NOTHING, db_column='id_blog')
    
    class Meta:
        managed = False
        db_table = 'foto_blog'
        
    def __str__(self):
        return f'{self.id_foto_blog} - {self.nombre_foto_blog} - {self.id_blog}'