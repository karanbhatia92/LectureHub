from django.conf.urls import include, url
from lecture_review_app import views as lecture_review_app_views

urlpatterns = [
    url(r'^login/', lecture_review_app_views.login, name = 'login'),
    url(r'^notes/', lecture_review_app_views.notes, name = 'notes'),
    url(r'^rating/', lecture_review_app_views.rating, name = 'rating'),
    url(r'^dashboard/', lecture_review_app_views.dashboard, name = 'dashboard'),
    url(r'^comment_dashboard/', lecture_review_app_views.comment_dashboard, name = 'comment_dashboard'),
    url(r'^course_dashboard/', lecture_review_app_views.course_dashboard, name = 'course_dashboard'),
    url(r'^generate_lecture_id/', lecture_review_app_views.generate_lecture_id, name = 'generate_lecture_id'),
    url(r'^logout/', lecture_review_app_views.logout, name = 'logout'),
]
