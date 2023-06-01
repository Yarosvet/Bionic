from .app import BionicApplication

app = None


def run_app():
    global app
    if app is None:
        app = BionicApplication()
