from ..cursor_position_tracker import _CURSOR_MARKER
from ..input_history import InputHistoryManager
from ..input_indexer import text_to_input_history_events
from ...utils.test import create_test_suite

def test_remove_selecting_single_events(assertion):
    input_history = InputHistoryManager()
    input_history.insert_input_events(text_to_input_history_events("Insert a new sentence. \n", "insert a new sentence"))
    input_history.insert_input_events(text_to_input_history_events("Insert a second sentence. \n", "insert a second sentence"))
    input_history.insert_input_events(text_to_input_history_events("Insert a third sentence.", "insert a third sentence"))
    input_history.cursor_position_tracker.text_history = """Insert a new sentence. 
Insert a second """ + _CURSOR_MARKER + """sentence. 
Insert a third sentence."""

    assertion( "    Selecting a single character to the left and remove it...")
    input_history.apply_key("shift:down left shift:up backspace")
    assertion( "        Expect history length to stay the same (3)", len(input_history.input_history) == 3)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index() 
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the same as before (10)", cursor_index[1] == 10)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[1].text == "Insert a secondsentence. \n")
    assertion( "        Expect phrase to be merged", input_history.input_history[1].phrase == "insert a secondsentence")
    assertion( "    Selecting three characters to the right and remove them...")
    input_history.apply_key("shift:down right:3 shift:up delete")
    assertion( "        Expect history length to stay the same (3)", len(input_history.input_history) == 3)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index() 
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the three less than before (7)", cursor_index[1] == 7)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[1].text == "Insert a secondtence. \n")
    assertion( "        Expect phrase to be merged", input_history.input_history[1].phrase == "insert a secondtence")
    assertion( "    Selecting right beyond the line break and remove the selection...")
    input_history.apply_key("shift:down right:10 shift:up backspace")
    assertion( "        Expect history length to be one less (2)", len(input_history.input_history) == 2)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the start of the next sentence (22)", cursor_index[1] == 22)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[1].text == "Insert a secondsert a third sentence.")
    assertion( "        Expect phrase to be merged", input_history.input_history[1].phrase == "insert a secondsert a third sentence")
    assertion( "    Selecting left beyond the line break and remove the selection...")
    input_history.apply_key("shift:down left:18 shift:up backspace")
    assertion( "        Expect history length to be one less (1)", len(input_history.input_history) == 1)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be the end of the sentence (22)", cursor_index[1] == 22)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[0].text == "Insert a new sentencesert a third sentence.")
    assertion( "        Expect phrase to be merged", input_history.input_history[0].phrase == "insert a new sentencesert a third sentence")

def test_remove_selecting_multiple_events_left(assertion):
    input_history = InputHistoryManager()
    input_history.insert_input_events(text_to_input_history_events("Suggest", "suggest"))
    input_history.insert_input_events(text_to_input_history_events(" create", "create"))
    input_history.insert_input_events(text_to_input_history_events(" delete", "delete"))
    input_history.insert_input_events(text_to_input_history_events(" insertion", "insertion"))
    input_history.cursor_position_tracker.text_history = "Suggest create delete insert" + _CURSOR_MARKER + "ion"

    assertion( "    Selecting characters until the left side of the event is reached and removing it...")
    input_history.apply_key("shift:down left:7 shift:up backspace")
    assertion( "        Expect history length to be one less (3)", len(input_history.input_history) == 3)
    assertion( input_history.input_history )
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be the same as before (3)", cursor_index[1] == 3)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[-1].text == " deleteion")
    assertion( "        Expect phrase to be merged", input_history.input_history[-1].phrase == "deleteion")
    assertion( "    Selecting characters until multiple events have been skipped over and removing it...")
    input_history.apply_key("shift:down left:14 shift:up backspace")
    assertion( "        Expect history length to be two less (1)", len(input_history.input_history) == 1)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be the same as before (3)", cursor_index[1] == 3)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[-1].text == "Suggestion")
    assertion( "        Expect phrase to be merged", input_history.input_history[-1].phrase == "suggestion")

def test_remove_selecting_multiple_events_right(assertion):
    input_history = InputHistoryManager()
    input_history.insert_input_events(text_to_input_history_events("Suggest ", "suggest"))
    input_history.insert_input_events(text_to_input_history_events("create ", "create"))
    input_history.insert_input_events(text_to_input_history_events("delete ", "delete"))
    input_history.insert_input_events(text_to_input_history_events("insertion", "insertion"))
    input_history.cursor_position_tracker.text_history = "Suggest" + _CURSOR_MARKER + " create delete insertion"
    assertion( "With a filled input history")
    assertion( "    Selecting characters until the right side of the event is reached and removing it...")
    input_history.apply_key("shift:down right shift:up backspace")
    assertion( "        Expect history length to be one less (3)", len(input_history.input_history) == 3)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index() 
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be one less than before same as before (23)", cursor_index[1] == 23)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[0].text == "Suggestcreate ")
    assertion( "        Expect phrase to be merged", input_history.input_history[0].phrase == "suggestcreate")
    assertion( "    Selecting characters until multiple events have been skipped over and removing it...")
    input_history.apply_key("shift:down right:20 shift:up backspace")
    assertion( "        Expect history length to be two less (1)", len(input_history.input_history) == 1)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 0", cursor_index[0] == 0)
    assertion( "        Expect cursor character index to be 20 less than before (3)", cursor_index[1] == 3)
    assertion( "        Expect no selection detected", input_history.is_selecting() == False)
    assertion( "        Expect text to be merged", input_history.input_history[-1].text == "Suggestion")
    assertion( "        Expect phrase to be merged", input_history.input_history[-1].phrase == "suggestion")

suite = create_test_suite("Removing selected text")
suite.add_test(test_remove_selecting_single_events)
suite.add_test(test_remove_selecting_multiple_events_left)
suite.add_test(test_remove_selecting_multiple_events_right)