from blinker import Signal  # type: ignore

application_setup_started = Signal("application-setup-started")
application_setup_finished = Signal("application-setup-finished")
application_routes_registered = Signal("application-routes-registered")
settings_configured = Signal("settings-configured")
request_started = Signal("request-started")
request_finished = Signal("request-finished")
