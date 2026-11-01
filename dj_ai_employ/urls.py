
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    path('orders/', include('orders.urls')),
]+debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


if settings.SHOW_DEBUGGER_TOOLBAR:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls')),
                    ]
#
# if settings.SHOW_SWAGGER:
#     urlpatterns += [
#         path('schema/', SpectacularAPIView.as_view(), name='schema'),
#         path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
#              name='swagger-ui'),
#     ]
