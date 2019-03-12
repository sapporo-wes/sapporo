# coding: utf-8
from .view_admin import AdminHomeView, AdminServiceView
from .view_auth import LoginNoPlaceholderView, SignupView
from .view_home import HomeView
from .view_run import RunDetailView, RunDownloadView, RunListView
from .view_service import ServiceDetailView, ServiceListView
from .view_workflow import (WorkflowDetailView, WorkflowListView,
                            WorkflowPrepareView)
