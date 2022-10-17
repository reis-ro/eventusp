from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .temp_data import movie_data
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404


from django.views import generic

from .models import Movie


# def list_movies(request):
#     movie_list = Movie.objects.all()
#     context = {'movie_list': movie_list}
#     return render(request, 'movies/index.html', context)

class MovieListView(generic.ListView):
    model = Movie
    template_name = 'movies/index.html'

# def list_movies(request):
#     context = {"movie_list": movie_data}
#     return render(request, 'movies/index.html', context)

# def detail_movie(request, movie_id):
#     movie = movie_data[movie_id - 1]
#     return HttpResponse(
#         f'Detalhes do filme {movie["name"]} ({movie["release_year"]})')

# def detail_movie(request, movie_id):
#     movie = Movie.objects.get(pk=movie_id)
#     context = {'movie': movie}
#     return render(request, 'movies/detail.html', context)

def detail_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    context = {'movie': movie}
    return render(request, 'movies/detail.html', context)

# def search_movies(request):
#     context = {}
#     if request.GET.get('query', False):
#         context = {
#             "movie_list": [
#                 m for m in movie_data
#                 if request.GET['query'].lower() in m['name'].lower()
#             ]
#         }
#     return render(request, 'movies/search.html', context)

def search_movies(request):
    context = {}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        movie_list = Movie.objects.filter(name__icontains=search_term)
        context = {"movie_list": movie_list}
    return render(request, 'movies/search.html', context)

# def create_movie(request):
#     if request.method == 'POST':
#         movie_data.append({
#             'name': request.POST['name'],
#             'release_year': request.POST['release_year'],
#             'poster_url': request.POST['poster_url']
#         })
#         return HttpResponseRedirect(
#             reverse('movies:detail', args=(len(movie_data), )))
#     else:
#         return render(request, 'movies/create.html', {})

def create_movie(request):
    if request.method == 'POST':
        movie_name = request.POST['name']
        movie_release_year = request.POST['release_year']
        movie_poster_url = request.POST['poster_url']
        movie = Movie(name=movie_name,
                      release_year=movie_release_year,
                      poster_url=movie_poster_url)
        movie.save()
        return HttpResponseRedirect(
            reverse('movies:detail', args=(movie.id, )))
    else:
        return render(request, 'movies/create.html', {})

def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == "POST":
        movie.name = request.POST['name']
        movie.release_year = request.POST['release_year']
        movie_poster_url = request.POST['poster_url']
        movie.save()
        return HttpResponseRedirect(
            reverse('movies:detail', args=(movie.id, )))

    context = {'movie': movie}
    return render(request, 'movies/update.html', context)


def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == "POST":
        movie.delete()
        return HttpResponseRedirect(reverse('movies:index'))

    context = {'movie': movie}
    return render(request, 'movies/delete.html', context)