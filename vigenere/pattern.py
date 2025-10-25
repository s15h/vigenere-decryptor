class Pattern:
    def __init__(self, pattern, spacing):
        self.pattern = pattern
        self.occurrences = 1
        self.spacing = spacing

    def add_occurrence(self):
        self.occurrences += 1