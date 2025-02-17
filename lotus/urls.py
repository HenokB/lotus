"""lotus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from metering_billing.views import auth_views, track
from metering_billing.views.model_views import (
    BillableMetricViewSet,
    BillingPlanViewSet,
    CustomerViewSet,
    InvoiceViewSet,
    PlanComponentViewSet,
    SubscriptionViewSet,
    UserViewSet,
)
from metering_billing.views.views import (
    CustomerWithRevenueView,
    InitializeStripeView,
    PeriodMetricRevenueView,
    PeriodMetricUsageView,
    PeriodSubscriptionsView,
)
from rest_framework import routers

from .settings import DEBUG, ON_HEROKU, PROFILER_ENABLED

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"metrics", BillableMetricViewSet, basename="metric")
router.register(r"plans", BillingPlanViewSet, basename="plan")
router.register(r"subscriptions", SubscriptionViewSet, basename="subscription")
router.register(r"components", PlanComponentViewSet, basename="component")
router.register(r"invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/track/", csrf_exempt(track.track_event), name="track_event"),
    path(
        "api/customer_summary/",
        CustomerWithRevenueView.as_view(),
        name="customer_summary",
    ),
    path(
        "api/period_metric_usage/",
        PeriodMetricUsageView.as_view(),
        name="period_metric_usage",
    ),
    path(
        "api/period_metric_revenue/",
        PeriodMetricRevenueView.as_view(),
        name="period_metric_revenue",
    ),
    path(
        "api/period_subscriptions/",
        PeriodSubscriptionsView.as_view(),
        name="period_subscriptions",
    ),
    path("api/stripe/", InitializeStripeView.as_view(), name="stripe_initialize"),
    path("api/login/", auth_views.login_view, name="api-login"),
    path("api/logout/", auth_views.logout_view, name="api-logout"),
    path("api/session/", auth_views.session_view, name="api-session"),
    path("api/whoami/", auth_views.whoami_view, name="api-whoami"),
]

if PROFILER_ENABLED:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

if DEBUG or ON_HEROKU:
    urlpatterns += [re_path(".*", TemplateView.as_view(template_name="index.html"))]
