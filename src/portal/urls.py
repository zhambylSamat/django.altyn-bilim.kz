"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/auth/', include(('portal.api.urls', 'portal'), namespace='authentication')),
    path('api/user/', include(('userInfo.api.urls', 'userInfo'), namespace='user')),
    path('api/group/lesson/', include(('groupsAndLessons.api.urls', 'groupsAndLessons'), namespace='groupsAndLessons')),
    path('api/lesson/progress/', include(('lessonProgress.api.urls', 'lessonProgress'), namespace='lessonProgress')),
    path('api/status/', include(('statuses.api.urls', 'statuses'), namespace='statuses')),
    path('api/materials/', include(('materials.api.urls', 'materials'), namespace='materials')),
    path('api/config/', include(('configuration.api.urls', 'configuration'), namespace='configuration')),
    path('api/payment/', include(('payment.api.urls', 'payment'), namespace="payment")),
    path('api/notification/prize/', include(('notificationAndPrize.api.urls', 'notificationAndPrize'), namespace="notificationAndPrize")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
