from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^download_file/(.+)/', 'sample.views.serve_mongo_download', name="download_file"),
)
