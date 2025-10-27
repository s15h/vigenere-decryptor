from vigenere.pattern import Pattern
import math
import vigenere.encryptor as encryptor

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
        max_key_length = 40
        for spacings in recurring.values():
            for spacing, pattern_obj in spacings.items():
                weight = pattern_obj.occurrences

                factors = self.get_factors(spacing, max_key_length)
                for factor in factors:
                    if 2 <= factor <= max_key_length:
                        spacing_counts[factor] = spacing_counts.get(factor, 0) + weight

        sorted_sizes = sorted(spacing_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_sizes


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
        cleaned_text = self.filter_invalid_characters(self.cipher_text.lower())
        
        # Check patterns of different sizes (longer patterns are more significant)
        for pattern_size in range(3, min(7, len(cleaned_text) // 2)):
            pattern_positions = {}
            
            # Build index of all patterns and their positions
            for i in range(len(cleaned_text) - pattern_size + 1):
                pattern = cleaned_text[i:i+pattern_size]
                if pattern not in pattern_positions:
                    pattern_positions[pattern] = []
                pattern_positions[pattern].append(i)
            
            # Find patterns that repeat and calculate spacings
            for pattern, positions in pattern_positions.items():
                if len(positions) > 1:
                    # Calculate all spacings between occurrences
                    for i in range(len(positions)):
                        for j in range(i + 1, len(positions)):
                            spacing = positions[j] - positions[i]
                            
                            if pattern not in recurring_patterns:
                                recurring_patterns[pattern] = {}
                            
                            if spacing not in recurring_patterns[pattern]:
                                recurring_patterns[pattern][spacing] = Pattern(pattern, spacing)
                            else:
                                recurring_patterns[pattern][spacing].add_occurrence()
        
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

    def get_bucket_distributions(self, key_length):
        from vigenere.encryptor import vig_dist
        cleaned_text = self.filter_invalid_characters(self.cipher_text.lower())
        return vig_dist(key_length, cleaned_text)

    def auto_decrypt(self, min_pct=17, max_pct=19, max_key_len=40):
        likely_key_sizes = [s for s, _ in self.determine_most_likely_key_sizes()]

        for size in likely_key_sizes:
            if size < 2 or size > max_key_len:
                continue
            dists = self.get_bucket_distributions(size)
            all_buckets_have_candidate_letter = True
            chosen_letters = []
            for bucket in dists:
                # check if there is are letters that might be the letter e
                candidates_letters = [ltr for ltr, pct in bucket.items() if pct >= min_pct and pct <= max_pct]
                if len(candidates_letters) != 1:
                    all_buckets_have_candidate_letter = False
                    break
                chosen_letters.append(candidates_letters[0])

            if all_buckets_have_candidate_letter:
                # Build encryption key assuming each chosen letter corresponds to plaintext 'e'
                alph = encryptor.ALPHABET
                key_chars = []
                for c in chosen_letters:
                    shift = (alph.index(c) - alph.index('e')) % 26
                    key_chars.append(alph[shift])
                found_key = ''.join(key_chars)
                decrypt_key = encryptor.vig_decryptkey(found_key)
                decrypted_msg = encryptor.vigenere(decrypt_key, self.cipher_text)
                return found_key, size, decrypted_msg

        return None, None, None

    @staticmethod
    def get_factors(n, max_factor):
        """Get all factors of n up to max_factor."""
        factors = []
        for i in range(2, min(int(math.sqrt(n)) + 1, max_factor + 1)):
            if n % i == 0:
                factors.append(i)
                if i != n // i and n // i <= max_factor:
                    factors.append(n // i)
        if n <= max_factor and n >= 2:
            factors.append(n)
        return factors
