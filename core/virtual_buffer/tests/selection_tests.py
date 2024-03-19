from ..buffer import VirtualBuffer
from ..indexer import text_to_virtual_buffer_tokens
from ...utils.test import create_test_suite

def selection_tests(assertion):
    test_selection(assertion, "which has often comforted the religious sceptic", "often", "often ")

def test_selection(assertion, buffer: str, query: str, result: str = ""):
    vb = VirtualBuffer()
    text_tokens = buffer.split(" ")
    tokens = []
    for index, text_token in enumerate(text_tokens):
        tokens.extend(text_to_virtual_buffer_tokens(text_token + (" " if index < len(text_tokens) - 1 else "")))

    vb.insert_tokens(tokens)
    assertion("    Starting with the text '" + buffer + "' and searching for '" + query + "'...")
    vb.select_phrases([x.phrase for x in text_to_virtual_buffer_tokens(query)])
    if result != "":
        assertion("        Should result in the selection '" + result.strip() + "'", vb.caret_tracker.get_selection_text().strip() == result.strip())
    else:
        assertion("        Should not result in a selection", vb.caret_tracker.selecting_text == False)

suite = create_test_suite("Selecting whole phrases inside of a selection") 
suite.add_test(selection_tests)
suite.run()