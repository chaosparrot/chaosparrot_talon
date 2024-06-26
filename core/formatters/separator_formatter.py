from typing import List
import re
from .text_formatter import TextFormatter

class SeparatorFormatter(TextFormatter):

    def __init__(self, name:str, separator = " "):
        super().__init__(name)
        self.separator = separator

    # Transform formatted text into separate words
    def format_to_words(self, text: str) -> List[str]:
        return self.split(text)
    
    # Transform words into the given format
    def words_to_format(self, words: List[str], previous: str = "", next: str = "") -> List[str]:
        append_character = ""
        if not (previous == "" or previous.endswith(self.separator) or not previous[-1].isalnum()):
            if len(words) == 0 or words[0][0].isalpha():
                append_character = self.separator

        # Add a character to the last word if it was the final one
        formatted = []
        if append_character:
            formatted.append(append_character)

        # Otherwise, just append the words with the separators together
        for index, word in enumerate(words):
            if index < len(words) - 1 and (word == "" or word[-1].isalpha()):
                should_append_separator = index + 1 >= len(words) or (words[index+1] == "" or words[index+1][0].isalnum())
                formatted.append(word + (self.separator if should_append_separator else ""))
            else:
                formatted.append(word)

        # Add the separator if the next, connected word does not have a separator
        if next and next[0].isalnum():
            formatted[-1] = formatted[-1] + self.separator

        return formatted
    
    def split(self, text: str, with_separator: bool = False) -> List[str]:
        separated_words = [word for word in text.split(self.separator)] if self.separator else [text]
        total_words = []
        for index, separated_word in enumerate(separated_words):
            appended_separator = (self.separator if with_separator and index != len(separated_words) - 1 else "")
            if separated_word.isalnum() or separated_word == "":
                total_words.append(separated_word + appended_separator)
            else:
                # Split non-alphanumeric characters in separate buckets
                new_word = ""
                new_words = []
                for char in separated_word:
                    if char.isalnum():
                        new_word += char
                    else:
                        if new_word:
                            new_words.append(new_word)
                            new_word = ""
                        new_words.append(char)
                if new_word:
                    new_words.append(new_word + appended_separator)
                
                total_words.extend(new_words)

        return total_words
    
    def split_format(self, text: str) -> List[str]:
        return self.split(text, True)