from django.shortcuts import redirect, render


def mainView(request):
    if request.user.is_authenticated:
      return redirect(to = "accounts/UserHome")
    return render(request,"OSheild/main.html")

def aboutAsView(request):
  return render(request,"OSheild/aboutUs.html")

