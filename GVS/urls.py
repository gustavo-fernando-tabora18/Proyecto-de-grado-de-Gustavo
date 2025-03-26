from django.urls import path
from . import views  # Espacio después del punto

app_name = 'GVS'

urlpatterns = [
    # Empresas
    path('empresa/', views.EmpresaListView.as_view(), name='empresa_list'),
    path('empresa/Crear/', views.EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresa/Editar/<int:pk>/', views.EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresa/eliminar/<int:pk>/', views.EmpresaDeleteView.as_view(), name='empresa_delete'),
    
    # URLs para Abanderado
    path('abanderado/', views.AbanderadoListView.as_view(), name='abanderado_list'),
    path('abanderado/crear/', views.AbanderadoCreateView.as_view(), name='abanderado_create'),
    path('abanderado/editar/<int:pk>/', views.AbanderadoUpdateView.as_view(), name='abanderado_update'),
    path('abanderado/eliminar/<int:pk>/', views.AbanderadoDeleteView.as_view(), name='abanderado_delete'),


    path('estacion/', views.EstacionListView.as_view(), name='estacion_list'),
    path('estacion/Crear/', views.EstacionCreateView.as_view(), name='estacion_create'),
    path('estacion/Editar/<int:pk>/', views.EstacionUpdateView.as_view(), name='estacion_update'),
    path('estacion/Eliminar/<int:pk>/', views.EstacionDeleteView.as_view(), name='estacion_delete'),

    path('empleado/', views.EmpleadoListView.as_view(), name='empleado_list'),
    path('empleado/Crear/', views.EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleado/Editar/<int:pk>/', views.EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleado/Eliminar/<int:pk>/', views.EmpleadoDeleteView.as_view(), name='empleado_delete'),

    path('solicitante/', views.SolicitanteListView.as_view(), name='solicitante_list'),
    path('solicitante/Crear/', views.SolicitanteCreateView.as_view(), name='solicitante_create'),
    path('solicitante/Editar/<int:pk>/', views.SolicitanteUpdateView.as_view(), name='solicitante_update'),
    path('solicitante/Eliminar/<int:pk>/', views.SolicitanteDeleteView.as_view(), name='solicitante_delete'),

    path('vacante/', views.VacanteListView.as_view(), name='vacante_list'),
    path('vacante/Crear/', views.VacanteCreateView.as_view(), name='vacante_create'),
    path('vacante/Editar/<int:pk>/', views.VacanteUpdateView.as_view(), name='vacante_update'),
    path('vacante/Eliminar/<int:pk>/', views.VacanteDeleteView.as_view(), name='vacante_delete'),

    # URLs para Entrevistador
    path('entrevistador/', views.EntrevistadorListView.as_view(), name='entrevistador_list'),
    path('entrevistador/Crear/', views.EntrevistadorCreateView.as_view(), name='entrevistador_create'),
    path('entrevistador/Editar/<int:pk>/', views.EntrevistadorUpdateView.as_view(), name='entrevistador_update'),
    path('entrevistador/Eliminar/<int:pk>/', views.EntrevistadorDeleteView.as_view(), name='entrevistador_delete'),

    # URLs para Entrevista
    path('entrevista/', views.EntrevistaListView.as_view(), name='entrevista_list'),
    path('entrevista/Crear/', views.EntrevistaCreateView.as_view(), name='entrevista_create'),
    path('entrevista/Editar/<int:pk>/', views.EntrevistaUpdateView.as_view(), name='entrevista_update'),
    path('entrevista/Eliminar/<int:pk>/', views.EntrevistaDeleteView.as_view(), name='entrevista_delete'),

    path('auditoria/', views.AuditoriaListView.as_view(), name='auditoria_list'),
    path('informe/', views.InformeListView.as_view(), name='informe_list'),
    path('informe/Crear/', views.InformeCreateView.as_view(), name='informe_create'),
    path('informe/Editar/<int:pk>/', views.InformeUpdateView.as_view(), name='informe_update'),
    path('informe/Eliminar/<int:pk>/', views.InformeDeleteView.as_view(), name='informe_delete'),


    

    # Index
    path('', views.index, name='index_base'),
] 