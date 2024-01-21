class View(object):
    def __init__(self, summary, template, time_stamp):
        self.summary = summary
        self.time_stamp = time_stamp
        self.template = template
    
    def render(self):
        with open(self.export_path, 'w') as f:
            f.write(self.html)