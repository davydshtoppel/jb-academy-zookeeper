from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings

from collections import OrderedDict
from datetime import datetime

from .models import NewsRepository


class MainView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class AllNewsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        news = NewsRepository.load_all(query)
        news_by_date = {}
        for it in news:
            time = it['created']
            time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            items = news_by_date.get(time.date())
            if items:
                items.append(it)
            else:
                news_by_date[time.date()] = [it]
        news_by_date = OrderedDict(sorted(news_by_date.items(), key=lambda x: x[0], reverse=True))
        return render(request, "news/all_news.html", context={'news_by_date': news_by_date})


class NewsView(View):
    def get(self, request, news_id, *args, **kwargs):
        news = NewsRepository.load_by_link(news_id)
        if news:
            return render(request, 'news/news.html', context=news)
        raise Http404


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create_news.html')

    def post(self, request, *args, **kwargs):
        NewsRepository.save_news(request.POST['title'], request.POST['text'])
        return redirect('/news/')
