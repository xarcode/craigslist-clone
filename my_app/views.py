import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://kolkata.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    #print(soup.prettify())

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_link = post.find('a').get('href')

        if(post.find(class_='result-price')):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            image_ids = post.find(class_='result-image').get('data-ids').split(',')
            req_img_id = image_ids[0]
            post_image = BASE_IMAGE_URL.format(req_img_id[2:])

        else:
            req_img_id = 'noneAtAll'
            #print(req_img_id)

        print(post_image)
        final_postings.append((post_title, post_link, post_price, post_image))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
