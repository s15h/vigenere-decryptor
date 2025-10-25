from vigenere.pattern import Pattern


class Cypher:
    def __init__(self, cypher_text):
        self.cypher_text = cypher_text
        self.possible_key_size = {}
        for i in range(2,27):
            self.possible_key_size[i] = 0

    def determine_most_likely_key_sizes(self):
        # count the possible common divisions of the spacings
        for pattern in self.get_recurring_patterns().values():
            for spacing, pattern_obj in pattern.items():
                for key_size in self.possible_key_size.keys():
                    if spacing % key_size == 0:
                        self.possible_key_size[key_size] += 1 * pattern_obj.occurrences

        probable_key_sizes = {}
        #strip out the key sizes that have no or low occurrences
        for key_size in self.possible_key_size:
            if self.possible_key_size[key_size] > 1:
                probable_key_sizes[key_size] = self.possible_key_size[key_size]
        self.possible_key_size = probable_key_sizes

        sorted_key_sizes = sorted(self.possible_key_size.items(), key=lambda x: x[1], reverse=True)
        return sorted_key_sizes



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
        text_length = len(self.cypher_text)

        for pattern_size in range(3,6):
            for i in range(0,text_length-pattern_size):
                pattern = self.cypher_text[i:i+pattern_size]
                if pattern.find(' ') != -1:
                    continue
                if pattern in single_patterns:
                    single_patterns[pattern].add(i)
                    for pattern_location in single_patterns[pattern]:
                        spacing = i - pattern_location
                        if spacing <= 0:
                            continue
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