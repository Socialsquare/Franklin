from debug_toolbar.panels import Panel


class LiveReloadPanel(Panel):
    name = "LiveReload"
    has_content = True
    template = "livereload.html"

    # log_data = None

    def title(self):
        return self.name

    def url(self):
        return ''
