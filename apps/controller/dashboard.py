import datetime as dt
import os

from apps.models.activity import Activity
from apps.models.operator import Operator
from apps.models.support import Support
from apps.models.summary import Summary
from apps.models.waiting_for_callback import WaitingForCallback
from apps.views.monitor_view import MonitorView
from apps.views.dashboard_view import DashboardView
from apps.views.performance_view import PerformanceView

import settings

def run_monitor():
    today = dt.date.today()

    activity_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_ACTIVITY_FILE)
    support_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_SUPPORT_FILE)
    close_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_CLOSE_FILE)

    activity = Activity(activity_file)
    support = Support(support_file)
    operator = Operator(close_file)
    wfc = WaitingForCallback(activity)

    summary = Summary(today, today, activity, support, operator, wfc, 'TVS')
    
    monitor_view = MonitorView(summary)
    monitor_view.get()
    monitor_view.render()

def run_dashboard(from_date, to_date, export_path):
    activity_file = os.path.join(settings.FILES_PATH, settings.TS_45DAYS_ACTIVITY_FILE)
    support_file = os.path.join(settings.FILES_PATH, settings.TS_45DAYS_SUPPORT_FILE)
    close_file = os.path.join(settings.FILES_PATH, settings.TS_45DAYS_CLOSE_FILE)

    activity = Activity(activity_file)
    support = Support(support_file)
    operator = Operator(close_file)
    wfc = WaitingForCallback(activity)

    summary = Summary(from_date, to_date, activity, support, operator, wfc, 'TVS')
    time_stamp=f"{from_date.strftime('%Y-%m-%d')} ～ {to_date.strftime('%Y-%m-%d')}"

    view_test = DashboardView(summary, export_path=export_path, time_stamp=time_stamp)
    view_test.render_html()

def run_today_dashboard():
    today = dt.date.today()

    activity_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_ACTIVITY_FILE)
    support_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_SUPPORT_FILE)
    close_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_CLOSE_FILE)

    activity = Activity(activity_file)
    support = Support(support_file)
    operator = Operator(close_file)
    wfc = WaitingForCallback(activity)

    summary = Summary(today, today, activity, support, operator, wfc, 'TVS')
    time_stamp = f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} 現在'
    
    dashboard = DashboardView(summary, time_stamp=time_stamp)
    dashboard.get()
    dashboard.render()

    monitor = MonitorView(summary, time_stamp=time_stamp)
    monitor.get()
    monitor.render()

    performance = PerformanceView(summary, time_stamp=time_stamp)
    performance.get()
    performance.render()
