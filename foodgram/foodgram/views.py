from django.shortcuts import render


def author(request):
    headline = 'Об авторе'
    text = 'Гришин Дмитрий - начинающий Python-разработчик.'
    github = 'https://github.com/nNDVG'
    instagram = 'https://www.instagram.com/grishinkrd/'
    return render(request, 'about.html', {'text': text, 'headline': headline, 'github': github, 'instagram': instagram})


def tech(request):
    headline = 'Технологии'
    text = 'Django, Django REST framework, PostgreSQL.'
    return render(request, 'about.html', {'text': text, 'headline': headline})


def page_not_found(request, exception):
    return render(request, '404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, '500.html', {'path': request.path}, status=500)