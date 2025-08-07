class BaseLoader:
    def __init__(self):
        self.context = {}
        self.results = []

    def process_country(self):
        # stub: simulate work
        import time; time.sleep(0.1)

    def post_process_country(self):
        pass

    def remove_deleted(self):
        pass

    @property
    def config(self):
        class C:
            def sync_deleted_records(self, loader):
                return False
        return C()