from ..cursor_position_tracker import CursorPositionTracker, _CURSOR_MARKER
from ..input_history import InputHistoryManager
from ..input_history_typing import InputHistoryEvent

input_history = InputHistoryManager()
input_history.insert_input_events(input_history.text_to_input_history_events("Insert a new sentence. \n", "insert a new sentence"))
input_history.insert_input_events(input_history.text_to_input_history_events("Insert a second sentence. \n", "insert a second sentence"))
input_history.insert_input_events(input_history.text_to_input_history_events("Insert a third sentence.", "insert a third sentence"))
input_history.cursor_position_tracker.text_history = """Insert a new sentence. 
Insert a second """ + _CURSOR_MARKER + """sentence. 
Insert a third sentence."""

print( "Inserting in between input events")
print( "    Inserting text into a filled input history...")    
input_history.insert_input_events(input_history.text_to_input_history_events("important ", "important"))
print( "        Expect history length to stay the same (3)", len(input_history.input_history) == 3)
cursor_index = input_history.cursor_position_tracker.get_cursor_index()
print( "        Expect cursor line index to be 1", cursor_index[0] == 1)
print( "        Expect cursor character index to be the same as before (10)", cursor_index[1] == 10)
input_index = input_history.determine_input_index()
print( "        Expect input index to be 1", input_index[0] == 1)
print( "        Expect input character index to be the length of the merged sentence minus the word sentence (26)", input_index[input_index[0]] == 26 )
print( "        Expect the phrase to be merged", input_history.input_history[input_index[0]].phrase == "insert a second important sentence" )
print( "        Expect the text to be merged", input_history.input_history[input_index[0]].text == "Insert a second important sentence. \n" )
print( "    Inserting a new line into the filled input history...") 
input_history.insert_input_events(input_history.text_to_input_history_events("\n", ""))
print( "        Expect history length to increase by one (4)", len(input_history.input_history) == 4) 
print( "        Expect split line to have an increased line index", input_history.input_history[2].line_index == 2)
print( "        Expect line after that to have increased its index as well", input_history.input_history[3].line_index == 3)
print( "        Expect the character index of the merged item to reset to 0", input_history.input_history[1].index_from_line_end == 0)
print( "        Expect the character index of the next to be the same", input_history.input_history[2].index_from_line_end == 0)
print( "    Inserting a word after the new line in the filled input history...")   
input_history.insert_input_events(input_history.text_to_input_history_events("Big ", "big")) 
print( "        Expect history length to increase by one (5)", len(input_history.input_history) == 5)
print( "        Expect line indexes to be the same", input_history.input_history[2].line_index == 2)
print( "        Expect the appended event to have a larger character index because it was added before words", input_history.input_history[2].index_from_line_end == 10)
print( "        Expect follow up events on the same line to have the same character index", input_history.input_history[3].index_from_line_end == 0)
print( "    Inserting another word after the new word in the filled input history...")   
input_history.insert_input_events(input_history.text_to_input_history_events("red ", "red"))
print( "        Expect history length to increase by one (6)", len(input_history.input_history) == 6)
print( "        Expect line indexes to be the same", input_history.input_history[3].line_index == 2)
print( "        Expect the appended event to have a larger character index because it was added before words", input_history.input_history[3].index_from_line_end == 10)
print( "        Expect the previous event to have a larger character index", input_history.input_history[2].index_from_line_end == 14)
print( "        Expect follow up events on the same line to have the same character index", input_history.input_history[4].index_from_line_end == 0)