from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib import messages




# Create your views here.

def post_list(request):
    template_name = 'post/post_list.html'
    posts = Post.objects.filter(deleted_at__isnull=True).order_by('-published_date')


    context = {
        'posts':posts
    }

    return render(request,template_name,context)



def create_post(request):
    
    template_name = 'post/create_post.html'
    form = PostForm
    context ={
        'form':form
    }
    return render(request,template_name,context)
    

def post_store(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author =  request.user  # convierte QueryDict a dict normal
        
            post.slug = slugify(f"{post.title}-{post.published_date}")
            
           
            post.save()

            # devolvemos el diccionario en formato JSON (sin guardar en BD)
            messages.success(request, "✅ Post creado correctamente.")
            return redirect('post:post_list')  # o donde quieras redirigir
        else:
            messages.error(request, "❌ No se pudo crear el post. Corrige los errores e inténtalo nuevamente.")
            
            # Volvemos a renderizar la misma vista con el formulario con errores
            return render(request, 'post/create_post.html', {'form': form})
                
    else:
        form = PostForm()
        return render(request, 'post/create_post.html', {'form': form})


def post_edit(request,slug):
    post =Post.objects.get(slug=slug) 
    template_name = 'post/post_edit.html'
    form = PostForm(instance=post)
    context = {
        'form': form,
        'post':post
    }

    return render(request,template_name,context)
        
def post_update(request,slug):

    post =Post.objects.get(slug=slug) 
    template_name = 'post/post_list'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited = form.save(commit=False)
            edited.author = request.user  # si quieres reasignar el autor
            edited.slug = slugify(f"{edited.title}-{edited.published_date}")
            edited.save()
            messages.success(request, "✅ Post actualizado correctamente.")
            return redirect('post:post_list')  # ✅ correcto


            
        else:
            messages.error(request, "❌ No se pudo crear el post. Corrige los errores e inténtalo nuevamente.")
            
            # Volvemos a renderizar la misma vista con el formulario con errores
            return render(request, template_name, {'form': form, 'post': post})


    else:
        form = PostForm(instance=post)
        return render(request, 'post/post_edit.html', {'form': form, 'post': post})

    

      

