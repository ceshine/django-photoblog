# -*- coding: utf-8 -*-
from datetime import datetime
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from photoblog.models import Photo

def index (request):
    try:
        photo = Photo.objects.filter(date_published__lte=datetime.now()).prefetch_related('tags').select_related('category', 'location').order_by('-date_published')[0]
    except:
        raise Http404

    return render(request, 'photoblog/index.html', {
        'photo': photo,
        'index': True,
        'date_as_title': getattr(settings, 'PHOTOBLOG_DATE_AS_TITLE', False),
        'extra_exif': getattr(settings, 'PHOTOBLOG_EXTRA_EXIF', False),
    })

@cache_page
def view_photo (request, id):
    photo = get_object_or_404(
        Photo.objects.prefetch_related('tags').select_related('category', 'location'),
        pk=id,
        date_published__lte=datetime.now()
    )

    return render(request, 'photoblog/index.html', {
        'photo': photo,
        'date_as_title': getattr(settings, 'PHOTOBLOG_DATE_AS_TITLE', False),
        'extra_exif': getattr(settings, 'PHOTOBLOG_EXTRA_EXIF', False),
    })

def archive (request):
    photos = Photo.objects.filter(date_published__lte=datetime.now()).prefetch_related('tags').select_related('category', 'location')

    per_page = getattr(settings, 'PHOTOBLOG_ARCHIVE_PER_PAGE', 30)
    orphans = per_page/3

    paginator = Paginator(photos, per_page=per_page, orphans=orphans)

    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    return render(request, 'photoblog/archive.html', {
        'photos': photos,
    })