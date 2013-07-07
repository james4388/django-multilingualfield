from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',
    url(r'^ckfiler/', 'multilingualfield.views.ckfiler', name='ckeditor_filer_browser'),
)
