from httpsrv.web.views import home, about

urlpatterns = [("/", home)]
urlpatterns = [("/", home), ("/about", about)]
