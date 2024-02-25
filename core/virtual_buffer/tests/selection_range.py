from ..buffer import VirtualBuffer
from ..indexer import text_to_virtual_buffer_tokens
from ...utils.test import create_test_suite

def test_select_single_word_and_extending(assertion):
    vb = VirtualBuffer()
    vb.insert_tokens(text_to_virtual_buffer_tokens("Insert ", "insert"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("a ", "a"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("new ", "new"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("sentence.", "sentence"))

    assertion( "    Selecting a single character to the left and then selecting 'Insert a'...")
    vb.apply_key("shift:down left shift:up")
    keys = vb.select_phrase("insert")
    keys = vb.select_phrase("a", True) 
    assertion( "        Should have the text 'Insert a ' selected", vb.caret_tracker.get_selection_text() == 'Insert a ')
    assertion( "        Should not deselect the previous selection", keys[0] not in ["left", "right"])
    assertion( "        Should go right 2 times to connect the end of 'Insert ' with 'a '", keys[0] == "shift-right:2")
    assertion( "    Deselecting, and then selecting 'Insert ' until 'new ' after that...")
    vb.select_phrase("insert")
    keys = vb.select_phrase("new", True) 
    assertion( "        Should have the text 'Insert a new ' selected", vb.caret_tracker.get_selection_text() == 'Insert a new ')
    assertion( "        Should not deselect the previous selection", keys[0] not in ["left", "right"])
    assertion( "        Should go right 6 times to connect the end of 'Insert ' with 'new '", keys[0] == "shift-right:6") 
    assertion( "    Selecting 'Insert ' and extend it until the end of the buffer...")
    keys = vb.select_until_end("insert")
    assertion( "        Should have the text 'Insert a new sentence.' selected", vb.caret_tracker.get_selection_text() == 'Insert a new sentence.')
    assertion( "        Should deselect the previous selection", keys[0] in ["left", "right"])
    assertion( "        Should go right 22 times to connect the end of 'Insert ' with 'sentence.'", keys[1] == "shift-right:22")
    assertion( "    Selecting 'new ' and extend it until the end of the buffer...")
    vb.select_phrase("new")
    keys = vb.select_until_end()
    assertion( "        Should have the text 'new sentence.' selected", vb.caret_tracker.get_selection_text() == 'new sentence.')
    assertion( "        Should not deselect the previous selection", keys[0] not in ["left", "right"])
    assertion( "        Should go right 9 times to connect the end of 'new ' with 'sentence.'", keys[0] == "shift-right:9")
    assertion( "    Selecting 'Insert ' using 'inssert' and extend it until the end of the buffer...")
    keys = vb.select_until_end("inssert")
    assertion( "        Should have the text 'Insert a new sentence.' selected", vb.caret_tracker.get_selection_text() == 'Insert a new sentence.')
    assertion( "        Should deselect the previous selection", keys[0] in ["left", "right"])
    assertion( "        Should go right 22 times to connect the end of 'Insert ' with 'sentence.'", keys[2] == "shift-right:22")

def test_selecting_multiple_phrases_with_duplicates(assertion):
    vb = VirtualBuffer()
    vb.insert_tokens(text_to_virtual_buffer_tokens("Insert ", "insert"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("a ", "a"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("new ", "new"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("sentence ", "sentence"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("or ", "or"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("insert ", "insert"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("a ", "a"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("new ", "new"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("paragraph.", "paragraph"))
    assertion( "    Selecting a single character to the left and then selecting 'insert a'...")
    vb.apply_key("shift:down left shift:up")
    vb.select_phrase("insert")
    keys = vb.select_phrase("a", True)
    assertion( "        Should have the text 'insert a ' selected", vb.caret_tracker.get_selection_text() == 'insert a ')
    assertion( "        Should not deselect the previous selection", keys[0] not in ["left", "right"])
    assertion( "        Should go right 2 times to connect the end of 'insert ' with 'a '", keys[0] == "shift-right:2")
    assertion( "    Selecting 'Insert ' by selecting 'insert' again, and then selecting 'a'...")
    vb.select_phrase("insert")
    vb.select_phrase("insert")
    keys = vb.select_phrase("a", True)
    assertion( "        Should have the text 'Insert a ' selected", vb.caret_tracker.get_selection_text() == 'Insert a ')
    assertion( "        Should not deselect the previous selection", keys[0] not in ["left", "right"])
    assertion( "        Should go right 2 times to connect the end of 'Insert ' with 'a ' beside it", keys[0] == "shift-right:2")
    assertion( "    Selecting 'Insert a new ' by continuing the selection with 'new'...")
    keys = vb.select_phrase("new", True)
    assertion( "        Should have the text 'Insert a new ' selected", vb.caret_tracker.get_selection_text() == 'Insert a new ')
    assertion( "        Should not deselect the previous selection", keys[0] not in ["left", "right"])
    assertion( "        Should go right 4 times to connect the end of 'a ' with 'new ' beside it", keys[0] == "shift-right:4")
    assertion( "    Selecting 'sentence or ' by starting the selection with 'or' and continuing it with 'sentence'...")
    vb.select_phrase("or")
    keys = vb.select_phrase("sentence", True)
    assertion( "        Should have the text 'sentence or ' selected", vb.caret_tracker.get_selection_text() == 'sentence or ')
    assertion( "        Should deselect the previous selection", keys[0] in ["left", "right"])
    assertion( "        Should move from the start of the previous selection to the beginning of the new selection", keys[1] == "left:9")
    assertion( "        And then go right until the selection has been made", keys[2] == "shift-right:12" )
    assertion( "    Selecting 'or ' by dragging the caret left, and then adding 'sentence '...")
    vb.select_phrase("or")
    vb.apply_key("right shift:down left:3 shift:up")
    keys = vb.select_phrase("sentence", True)
    assertion( "        Should have the text 'sentence or' selected", vb.caret_tracker.get_selection_text() == 'sentence or ')
    assertion( "        Should not deselect the previous selection", keys[0] not in ["left", "right"])
    assertion( "        Should move from the start of the previous selection to the beginning of the new selection", keys[0] == "shift-left:9")
    assertion( "    Selecting 'or ' by dragging the caret left, and then adding 'insert '...")
    vb.select_phrase("or")
    vb.apply_key("right shift:down left:3 shift:up")
    keys = vb.select_phrase("insert", True)
    assertion( "        Should have the text 'or insert ' selected", vb.caret_tracker.get_selection_text() == 'or insert ')
    assertion( "        Should deselect the previous selection", keys[0] in ["left", "right"] )
    assertion( "        And then should move from the start of the previous selection to the end of the new selection", keys[1] == "shift-right:10")

def test_select_phrase_inside_selection_with_duplicates(assertion):
    vb = VirtualBuffer()
    vb.insert_tokens(text_to_virtual_buffer_tokens("Insert ", "insert"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("a ", "a"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("new ", "new"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("sentence ", "sentence"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("or ", "or"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("insert ", "insert"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("a ", "a"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("new ", "new"))
    vb.insert_tokens(text_to_virtual_buffer_tokens("paragraph.", "paragraph"))
    assertion( "    Selecting 'or insert a ' and then selecting 'insert'...")
    vb.select_phrase("or")
    vb.select_phrase("insert", True)
    vb.select_phrase("new", True)
    keys = vb.select_phrase("insert")
    assertion( "        Should have the text 'insert ' selected", vb.caret_tracker.get_selection_text() == 'insert ')
    assertion( "        Should deselect the previous selection", keys[0] in ["left", "right"])
    assertion( "        Should go right 3 times to go to the start of 'insert'", keys[1] == "right:3")
    assertion( "        And then go right until 'insert ' is selected", keys[2] == "shift-right:7")

suite = create_test_suite("Selection range after words")
suite.add_test(test_select_single_word_and_extending)
suite.add_test(test_selecting_multiple_phrases_with_duplicates)
suite.add_test(test_select_phrase_inside_selection_with_duplicates) 