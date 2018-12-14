from bs4 import BeautifulSoup as bs
import requests
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


def main(request):


    return render(request,
                  'hu/main.html',


                  {}

    )

def sign_in(request):
    return render(request,
                  'hu/sign_in.html'

    )


def register(request):
    return render(request,
                  'hu/register.html'

                  )


def forgot(request):
    return render(request,
                  'hu/forgot-password.html'

                  )


@login_required
def comment(request):
    if request.method =='GET':
        return render(request, 'hu/comment.html',{})
    else:
        comment = request.POST['comment']

        member = Comment(comment = comment)
        member.save()
    return HttpResponse('입력완료')





def post(request):


    # reddit
    browser = webdriver.Chrome('/Users/rexypark/Desktop/chromedriver')
    browser.get('https://www.reddit.com/r/popular')

    time.sleep(1)
    elm = browser.find_element_by_tag_name('html')
    elm.send_keys(Keys.END)

    time.sleep(1)
    elm.send_keys(Keys.END)

    time.sleep(1)
    elm.send_keys(Keys.END)

    time.sleep(1)
    elm.send_keys(Keys.END)

    soup = bs(browser.page_source, 'html.parser')
    tag_list = soup.select('span > a[href]')

    urL = []
    titles = []
    homePages = []

    for i in range(0, len(tag_list)):
        try:
            titles.append(tag_list[i].select('h2')[0].get_text())
            urL.append('https://www.reddit.com' + tag_list[i]['href'])
            r = 'reddit'
            homePages.append(r)
        except (SyntaxError, IndexError):
            pass


        # cheezBuger
    for i in range(2, 3):
        html = requests.get('https://cheezburger.com/page/' + str(i))
        soup = bs(html.text, 'html.parser')
        urlWay = soup.select('.title-sharing-buttons a')

        for u in range(0, len(urlWay)):
            titles.append(urlWay[i].select('span')[0].get_text())
            urL.append(urlWay[i]['href'])
            c = 'cheezBuger'
            homePages.append(c)

    browser = webdriver.Chrome('/Users/rexypark/Desktop/chromedriver')
    browser.get('https://9gag.com/hot')

    time.sleep(1)
    elm = browser.find_element_by_tag_name('html')
    elm.send_keys(Keys.END)

    time.sleep(1)
    elm.send_keys(Keys.END)

    time.sleep(1)
    elm.send_keys(Keys.END)

    time.sleep(1)
    elm.send_keys(Keys.END)

    soup = bs(browser.page_source, 'html.parser')
    res = soup.select('article[id]')
    res_name = soup.select('article[id] h1')


    for i in range(0, len(res)):
        urL.append('https://9gag.com' + res[i].select('a')[2]['href'])

    for l in range(0, len(res_name)):
        titles.append(res_name[l].get_text())
        h = '9gag'
        homePages.append(h)

    for t in range(len(titles)):


        title = titles[t]
        url = urL[t]
        homePage = homePages[t]

        Post.objects.create(title = title, url = url, homePage = homePage,date=timezone.now())

    return HttpResponse('ok')


def show(request):
    page = '1'
    try:
        page = request.GET['page']
    except MultiValueDictKeyError as e:
        pass
    board_list = Post.objects.order_by('-id')  #Board는 데이터 넣는 클래스명. -id는 id의 역순으로 order_by정렬
    paginator = Paginator(board_list, 10)  #페이지 분할
    page_info = paginator.page(page)
    start_page = (int(page) - 1) // 10 * 10 + 1
    end_page = start_page + 10
    if end_page > page_info.paginator.num_pages:
        end_page = page_info.paginator.num_pages
    page_list = range(start_page, end_page)

    prev_page = start_page - 10
    next_page = start_page + 10
    return render(
        request,
        'hu/main.html',
        {
            'start_page': int(start_page),
            'end_page': int(end_page),
            'page_info': page_info,
            'page_list': page_list,
            'page': int(page),
            'next_page': next_page,
            'prev_page': prev_page
        }


    )
