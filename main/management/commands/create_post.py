from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import Post
import argparse


class Command(BaseCommand):
    help = 'Create a new blog post from command line'

    def add_arguments(self, parser):
        parser.add_argument('--title', type=str, required=True, help='Post title')
        parser.add_argument('--content', type=str, required=True, help='Post content')
        parser.add_argument('--excerpt', type=str, help='Post excerpt (optional)')
        parser.add_argument('--image', type=str, help='Image URL (optional)')
        parser.add_argument('--published', action='store_true', help='Publish immediately')

    def handle(self, *args, **options):
        title = options['title']
        content = options['content']
        excerpt = options.get('excerpt', '')
        image_url = options.get('image', '')
        published = options.get('published', False)

        # Create the post
        post = Post.objects.create(
            title=title,
            content=content,
            excerpt=excerpt,
            published_date=timezone.now() if published else None
        )

        if image_url:
            # Note: This is a simplified approach. In production, you'd want to download and save the image
            post.image = image_url
            post.save()

        status = "published" if published else "draft"
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {status} post: "{title}"')
        ) 