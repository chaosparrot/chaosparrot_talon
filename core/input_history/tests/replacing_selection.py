from ..cursor_position_tracker import _CURSOR_MARKER
from ..input_history import InputHistoryManager
from ...utils.test import create_test_suite

input_history = InputHistoryManager()
input_history.insert_input_events(input_history.text_to_input_history_events("Insert a new sentence. \n", "insert a new sentence"))
input_history.insert_input_events(input_history.text_to_input_history_events("Insert a second sentence. \n", "insert a second sentence"))
input_history.insert_input_events(input_history.text_to_input_history_events("Insert a third sentence.", "insert a third sentence"))
input_history.cursor_position_tracker.text_history = """Insert a new sentence. 
Insert a second """ + _CURSOR_MARKER + """sentence. 
Insert a third sentence."""

def test_single_event_replacement(assertion):
    assertion( "    Selecting a single character to the left and replace it...")
    input_history.apply_key("shift:down left shift:up")
    input_history.insert_input_events(input_history.text_to_input_history_events("G"))
    assertion( "        Expect history length to stay the same (3)", len(input_history.input_history) == 3)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index() 
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the same as before (10)", cursor_index[1] == 10)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[1].text == "Insert a secondGsentence. \n")
    assertion( "        Expect phrase to be merged", input_history.input_history[1].phrase == "insert a secondgsentence")
    assertion( "    Selecting a single character to the right and replace it...")
    input_history.apply_key("shift:down right shift:up")
    input_history.insert_input_events(input_history.text_to_input_history_events("G"))
    assertion( "        Expect history length to stay the same (3)", len(input_history.input_history) == 3)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be one more than before (9)", cursor_index[1] == 9)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[1].text == "Insert a secondGGentence. \n")
    assertion( "        Expect phrase to be merged", input_history.input_history[1].phrase == "insert a secondggentence")
    assertion( "    Selecting right beyond the line break and replace the selection...")
    input_history.apply_key("left shift:down right:11 shift:up")
    input_history.insert_input_events(input_history.text_to_input_history_events(" and "))
    assertion( "        Expect history length to be the one more than before (4)", len(input_history.input_history) == 4)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the start of the next sentence (24)", cursor_index[1] == 24)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "    Selecting left beyond the line break and replace the selection...")
    input_history.apply_key("shift:down left:5 left:17 shift:up")
    input_history.insert_input_events(input_history.text_to_input_history_events("But also... "))
    assertion( "        Expect history length to be the one less than before (3)", len(input_history.input_history) == 3)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be the middle of the joined sentence (24)", cursor_index[1] == 24)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)

def test_multiple_event_replacement_left(assertion):
    input_history = InputHistoryManager()
    input_history.insert_input_events(input_history.text_to_input_history_events("Suggest", "suggest"))
    input_history.insert_input_events(input_history.text_to_input_history_events(" create", "create"))
    input_history.insert_input_events(input_history.text_to_input_history_events(" delete", "delete"))
    input_history.insert_input_events(input_history.text_to_input_history_events(" insertion", "insertion"))
    input_history.cursor_position_tracker.text_history = "Suggest create delete insert" + _CURSOR_MARKER + "ion"

    assertion( "    Selecting characters until the left side of the event is reached and replacing it...")
    input_history.apply_key("shift:down left:7 shift:up")
    input_history.insert_input_events(input_history.text_to_input_history_events("rat"))
    assertion( "        Expect history length to be one less (3)", len(input_history.input_history) == 3)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0) 
    assertion( "        Expect cursor character index to be the same as before (3)", cursor_index[1] == 3)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[-1].text == " deleteration")
    assertion( "        Expect phrase to be merged", input_history.input_history[-1].phrase == "deleteration")
    assertion( "    Selecting characters until multiple events have been skipped over and replacing it...")
    input_history.apply_key("shift:down left:17 shift:up") 
    input_history.insert_input_events(input_history.text_to_input_history_events("ilat"))
    assertion( "        Expect history length to be two less (1)", len(input_history.input_history) == 1)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index() 
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be the same as before (3)", cursor_index[1] == 3)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[-1].text == "Suggestilation")
    assertion( "        Expect phrase to be merged", input_history.input_history[-1].phrase == "suggestilation")

def test_multiple_event_replacement_right(assertion):
    input_history = InputHistoryManager()
    input_history.insert_input_events(input_history.text_to_input_history_events("Suggest ", "suggest"))
    input_history.insert_input_events(input_history.text_to_input_history_events("create ", "create"))
    input_history.insert_input_events(input_history.text_to_input_history_events("delete ", "delete"))
    input_history.insert_input_events(input_history.text_to_input_history_events("insertion", "insertion"))
    input_history.cursor_position_tracker.text_history = "Suggest" + _CURSOR_MARKER + " create delete insertion"
    assertion( "    Selecting characters until the right side of the event is reached and replacing it...")
    input_history.apply_key("shift:down right shift:up")
    input_history.insert_input_events(input_history.text_to_input_history_events("or"))
    assertion( "        Expect history length to be one less (3)", len(input_history.input_history) == 3)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be the same as before (23)", cursor_index[1] == 23)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[0].text == "Suggestorcreate ")
    assertion( "        Expect phrase to be merged", input_history.input_history[0].phrase == "suggestorcreate")
    assertion( "    Selecting characters until multiple events have been skipped over and replacing it...")
    input_history.apply_key("shift:down right:20 shift:up")
    input_history.insert_input_events(input_history.text_to_input_history_events("in"))
    assertion( "        Expect history length to be two less (1)", len(input_history.input_history) == 1)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be 20 less than before (3)", cursor_index[1] == 3)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[-1].text == "Suggestorinion")
    assertion( "        Expect phrase to be merged", input_history.input_history[-1].phrase == "suggestorinion")

suite = create_test_suite("Replacing selection with new text")
suite.add_test(test_single_event_replacement)
suite.add_test(test_multiple_event_replacement_left)
suite.add_test(test_multiple_event_replacement_right)
