class Item:
    def __init__(self, url, tries=0):
        self.url = url
        self.start = None
        self.tries = tries
