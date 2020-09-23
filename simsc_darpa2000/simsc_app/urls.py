from django.conf.urls import url

from simsc_app import views

urlpatterns = [
    url(r'^$', views.SimscAutoView.as_view(), name='link_main'),
    #url(r'^graph/(?P<n_cluster>\d+)/(?P<n_commonip>\d+)/(?P<n_timedif>\d+)/$', views.generate_flow_graph, name='flow_graph'),
    url(r'^graph/$', views.generate_graph, name='link_graph'),
    url(r'^graph/data$', views.data_graph, name='link_data_graph'),
    url(r'^stats/$', views.generate_stats, name='link_stats'),
]
