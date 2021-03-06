from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from blog.models import Post


def post_list(request):
    # Template를 찾을 경로에서 post_list.html을 찾아서
    # 그 파일을 text로 만들어서 HttpResponse 형태로 돌려준다.
    # 위 기능을 하는 shortcut 함수

    # 1. posts라는 변수에 전체 Post를 가지는 QuerySet 객체를 할당
    #   hint) Post.objects.무언가... 를 실행한 결과는 QuerySet 객체가 된다.
    # 2. context라는 dict를 생성하며, 'post'키에 위에 posts변수를 value로 사용하도록 한다.
    # 3. render의 3번째 위치인자로 위 context 변수를 전달한다.

    # posts = Post.objects.all()
    posts = Post.objects.order_by('-pk')
    context = {'posts': posts}

    return render(request, 'post_list.html', context)

def post_detail(request, pk):
    print("post_detail request", request)
    print("post_detail pk", pk)

    # URL: /post-detail/
    # View: post_detail
    # Template: post_detail.html
    # 내용으로 <h1>Post Detail!</h1>을 갖도록 함

    # 1. 전체 Post목록(Post 전체 QuerySet) 중 [0]번 index에 해당하는 Post객체 하나를 post 변수에 할당
    # 2. 'context'라는 이름의 dict 만들기, 'post' key에 위 post변수를 value로 사용한다.

    # 이 view 함수의 매개변수로 전달되는 'pk'를 사용해서
    # 전달받은 'pk'값이 자신의 'pk' DB Column값과 같은 Post를 post 변수에 지정
    # 이후 pk에 따라 /post-detail/에 접근했을 때, 다른 Post가 출력되는지 확인

    # posts = Post.objects.filter(pk=pk)
    # post = posts[0]

    # try-except 구문을 사용해서 pk에 해당하는 Post가 없는 경우,
    # HttpResponse('없음')을 돌려주도록 함

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse('없음')

    # post = get_object_or_404(Post, pk=pk)

    # 3. 이 context 변수를 render의 3번째 인자로 전달
    # 4. post_detail.html에서는 전달받은 'post' 변수의 title, author, text, created_date, published_date를 적절히 출력한다.

    context = {'post': post,}

    return render(request, 'post_detail.html', context)

def post_add(request):
    if request.method == 'POST':
        # request.POST에 담긴 title, text를
        # HttpResponse를 사용해서 적절히 리턴
        # title:<입력받은 제목> text: <입력받은 텍스트>
        author = request.user
        title = request.POST['title']
        text = request.POST['text']

        # 위 3개의 값을 사용해서 새로운 Post 생성
        # 생성한 Post의 title과 created_date를 HttpResponse에 적절한 문자열로 전달
        # 출력 예) title: 파이썬, created_date: <적당한 값>

        post = Post.objects.create(
            title=title,
            author=author,
            text=text,
        )

        # result = f'title: {post.title}, created_date: {post.created_date}'

        # post_list_url = reverse('url-name-post-list')
        # return HttpResponseRedirect(post_list_url)

        return redirect('url-name-post-list')

    else:
        # URL: /posts/add
        # View: 이 함수
        # Template: post_add.html
        # form 태그 내부에
        # input, textarea, button[type=submit]
        # base.html의 nav 안에 /posts/add/로의 링크 하나 추가
        # 링크 텍스트 Post Add
        return render(request, 'post_add.html')

# 숙제

def post_delete(request, pk):
    # pk에 해당하는 Post를 삭제한다
    # 삭제 후에는 post_list페이지로 이동
    Post.objects.filter(pk=pk).delete()

    return redirect('url-name-post-list')

def post_edit(request, pk):
    # pk에 해당하는 Post를 수정한다
    if request.method == 'POST':
        # request.POST로 전달된 title, text내용을 사용해서
        #  pk에 해당하는 Post의 해당 필드를 수정하고 save()
        #  이후 해당 Post의 post-detail화면으로 이동

        post = get_object_or_404(Post, pk=pk)

        title = request.POST['title']
        text = request.POST['text']

        post.title = title
        post.text = text

        post.save()

        return redirect('url-name-post-detail',pk=post.pk)
    else:
        # 수정할 수 있는 form이 존재하는 화면을 보여줌
        # 화면의 form에는 pk에 해당하는 Post의 title, text값이 들어있어야 함 (수정이므로)
        post = Post.objects.get(pk=pk)

        context = {
            'post' : post,
        }

        return render(request, 'post_edit.html', context)


def post_publish(request, pk):
    # pk에 해당하는 Post의 published_date를 업데이트
    # 요청시점의 시간을 해당 Post의 published_date에 기록할 수 있도록 한다
    # 완료후에는 post-detail로 이동
    #  결과를 볼 수 있도록, 리스트 및 디테일 화면에서 published_date도 출력하도록 한다
    return redirect('url-name-post-detail', pk=post.pk)

def post_unpublish(request, pk):
    # pk에 해당하는 Post의 published_date에 None을 대입 후 save()
    # 완료후에는 post-detail로 이동
    #  결과를 볼 수 있도록, 리스트 및 디테일 화면에서 published_date도 출력하도록 한다
    return redirect('url-name-post-detail', pk=post.pk)