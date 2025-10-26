from vigenere.pattern import Pattern
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

class Cipher:
    def __init__(self, cipher_text):
        self.cipher_text = cipher_text
        self.possible_key_size = {}
        for i in range(2,27):
            self.possible_key_size[i] = 0

    def determine_most_likely_key_sizes(self):
        recurring = self.get_recurring_patterns()
        spacing_counts = {}
        for spacings in recurring.values():
            for spacing, pattern_obj in spacings.items():
                spacing_counts[spacing] = spacing_counts.get(spacing, 0) + pattern_obj.occurrences
        sorted_spacings = sorted(spacing_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_spacings


    def get_repeating_patterns(self):
        recurring_patterns = self.get_recurring_patterns()
        flattened_patterns = []
        for pattern, spacings in recurring_patterns.items():
            for spacing, pattern_obj in spacings.items():
                flattened_patterns.append(pattern_obj)
        sorted_repeated_patterns = sorted(flattened_patterns, key=lambda p: p.occurrences, reverse=True)
        return sorted_repeated_patterns

    def get_recurring_patterns(self):
        recurring_patterns = {}
        single_patterns = {}
        text_length = len(self.cipher_text)

        for pattern_size in range(3,4):
            for i in range(0,text_length-pattern_size):
                pattern = self.cipher_text[i:i+pattern_size]
                if self.string_contains_invalid_characters(pattern):
                    continue
                if pattern in single_patterns:
                    single_patterns[pattern].add(i)
                    for pattern_location in single_patterns[pattern]:
                        if pattern_location == i:
                            continue
                        spacing_text = self.cipher_text[pattern_location:i]
                        spacing = len(self.filter_invalid_characters(spacing_text))
                        if pattern in recurring_patterns:
                            if spacing in recurring_patterns[pattern]:
                                recurring_patterns[pattern][spacing].add_occurrence()
                            else:
                                recurring_patterns[pattern][spacing] = Pattern(pattern, spacing)
                        else:
                            recurring_patterns[pattern] = {}
                            recurring_patterns[pattern][spacing] = Pattern(pattern, spacing)
                else:
                    single_patterns[pattern] = {i}
        return recurring_patterns

    @staticmethod
    def string_contains_invalid_characters(string):
        for i in string:
            if i.lower() not in ALPHABET:
                return True
        return False

    @staticmethod
    def filter_invalid_characters(string):
        return ''.join(filter(lambda x: x.lower() in ALPHABET, string))