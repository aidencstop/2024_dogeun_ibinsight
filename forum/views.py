from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post, Category, Hashtags
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Comment

categories = [
    "Group 1: Studies in Language and Literature",
    "Group 2: Language Acquisition",
    "Group 3: Individuals and Societies",
    "Group 4: Sciences",
    "Group 5: Mathematics",
    "Group 6: The Arts",
    "Others: Non IB Related"
]
for name in categories:
    Category.objects.get_or_create(name=name)

from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post, Category, Hashtags
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        hashtags = request.POST['hashtags'].split(',')  # Split hashtags by comma
        categories = request.POST.getlist('category')  # Get the list of selected categories

        post = Post(title=title, content=content, created_by=None)
        post.save()  # Save the post first to get an ID

        # Handle hashtags if needed
        for tag in hashtags:
            hashtag, created = Hashtags.objects.get_or_create(name=tag.strip())
            post.hashtags.add(hashtag)

        # Add categories
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            post.categories.add(category)

        return redirect('forum_list')  # Redirect to the forum list or another page

    return render(request, 'forum/writeforum.html')

def forum_list(request):
    categories = Category.objects.all()  # Get all categories for filtering
    selected_categories = request.GET.getlist('categories')  # Get selected categories from request

    # Filter posts by selected categories if any
    if selected_categories:
        posts = Post.objects.filter(categories__in=selected_categories).distinct()
    else:
        posts = Post.objects.all()

    context = {
        'posts': posts,
        'categories': categories,  # Pass categories to the template for filtering
    }
    return render(request, 'forum/forum.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)  # Fetch comments related to the post

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        # Create a comment with user as None if not authenticated
        Comment.objects.create(post=post, user=request.user if request.user.is_authenticated else None, text=comment_text)
        return redirect('post_detail', id=post.id)

    return render(request, 'forum/moredetail.html', {'post': post, 'comments': comments})
