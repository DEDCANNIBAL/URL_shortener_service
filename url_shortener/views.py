from random import choices
from string import ascii_letters, digits
from urllib.parse import urlparse

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views import View

from url_shortener.models import ShortUrl


class MainPage(View):
    paginate_by = 30
    template_name = 'index.html'
    alphabet = ascii_letters + digits
    short_url_length = ShortUrl.short_url.field.max_length

    def get(self, request, *args, **kwargs):
        context = {'short_url': request.GET.get('short_url')}
        if request.user.is_authenticated:
            context['short_urls_page'] = self.get_current_short_urls_page(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        origin_url = self.request.POST['origin_url']
        if not urlparse(origin_url).netloc:
            messages.add_message(request, messages.ERROR, 'URL is not valid.')
            return HttpResponseRedirect("/")
        owner = request.user if self.request.user.is_authenticated else None
        short_url = self.generate_short_url()
        ShortUrl.objects.create(
            short_url=short_url,
            origin_url=origin_url,
            owner=owner
        )
        return redirect(f"/?short_url={short_url}")

    def get_current_short_urls_page(self, request):
        owner = request.user
        shortened_urls_list = ShortUrl.objects.filter(owner=owner)
        paginator = Paginator(shortened_urls_list, self.paginate_by)
        page = request.GET.get('page')
        return paginator.get_page(page)

    def generate_short_url(self):
        short_url = self.generate_id()
        while ShortUrl.objects.filter(short_url=short_url).exists():
            short_url = self.generate_id()
        return short_url

    def generate_id(self):
        return ''.join(choices(self.alphabet, k=self.short_url_length))


def redirect_by_short_url(request, short_url):
    with transaction.atomic():
        short_url_obj = ShortUrl.objects.filter(short_url=short_url).select_for_update().last()
        if short_url_obj is None:
            raise Http404("Short URL does not exist.")
        short_url_obj.click_counter += 1
        short_url_obj.save()
    return redirect(short_url_obj.origin_url)
