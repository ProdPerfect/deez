from blinker import signal  # type: ignore

application_setup_started = signal('application-setup-started')
application_setup_finished = signal('application-setup-finished')
application_routes_registered = signal('application-routes-registered')
