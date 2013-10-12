# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_paginator(request, object_list, num_per_page):
    paginator = Paginator(object_list, num_per_page)
    page = request.GET.get('page')
    try:
        ret = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ret = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ret = paginator.page(paginator.num_pages)
    return ret
