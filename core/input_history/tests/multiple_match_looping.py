from ..cursor_position_tracker import CursorPositionTracker, _CURSOR_MARKER
from ..input_history import InputHistoryManager
from ..input_history_typing import InputHistoryEvent

def get_filled_ihm():
    ihm = InputHistoryManager()
    ihm.insert_input_events(ihm.text_to_input_history_events("Insert ", "insert"))
    ihm.insert_input_events(ihm.text_to_input_history_events("a ", "a"))
    ihm.insert_input_events(ihm.text_to_input_history_events("new ", "new"))
    ihm.insert_input_events(ihm.text_to_input_history_events("sentence, ", "sentence"))
    ihm.insert_input_events(ihm.text_to_input_history_events("that ", "that"))
    ihm.insert_input_events(ihm.text_to_input_history_events("will ", "will"))
    ihm.insert_input_events(ihm.text_to_input_history_events("have ", "have"))
    ihm.insert_input_events(ihm.text_to_input_history_events("new ", "new"))
    ihm.insert_input_events(ihm.text_to_input_history_events("words ", "words"))
    ihm.insert_input_events(ihm.text_to_input_history_events("compared ", "compared"))
    ihm.insert_input_events(ihm.text_to_input_history_events("to ", "to"))
    ihm.insert_input_events(ihm.text_to_input_history_events("the ", "the"))
    ihm.insert_input_events(ihm.text_to_input_history_events("previous ", "previous"))
    ihm.insert_input_events(ihm.text_to_input_history_events("sentence.", "sentence"))
    return ihm

input_history = get_filled_ihm()
print( "Using a filled input history which contains duplicates of certain words")
print( "    Moving from the end to the history to the last occurrence of 'sentence'...") 
keys = input_history.go_phrase("sentence", 'start')
print( "        Should go left until the last occurrence of sentence", keys[0] == "left:9")
print( "    Repeating the search for 'sentence'...") 
keys = input_history.go_phrase("sentence", 'start')
print( "        Should go left until the first occurrence of sentence", keys[0] == "left:60")
print( "    Repeating the search for 'sentence' again...") 
keys = input_history.go_phrase("sentence", 'start')
print( "        Should loop back to the last occurrence", keys[0] == "right:60")
print( "    Repeating the search for 'sentence' once more...")
keys = input_history.go_phrase("sentence", 'start')
print( "        Should loop back to the first occurrence", keys[0] == "left:60")

input_history = get_filled_ihm()
print( "Using a filled input history which contains duplicates of certain words")
print( "    Moving from the end to the history to the last occurrence of 'sentence'...") 
keys = input_history.go_phrase("sentence", 'end')
print( "        Should not move anywhere as we are already at the end", len(keys) == 0)
print( "    Repeating the search for 'sentence'...")
keys = input_history.go_phrase("sentence", 'end')
print( "        Should go left until the first occurrence of sentence", keys[0] == "left:59")
print( "    Repeating the search for 'sentence' again...")
keys = input_history.go_phrase("sentence", 'end')
print( "        Should loop back to the last occurrence", keys[0] == "right:59")
print( "    Repeating the search for 'sentence' once more...")
keys = input_history.go_phrase("sentence", 'end')
print( "        Should loop back to the first occurrence", keys[0] == "left:59")

input_history = get_filled_ihm()
print( "Using a filled input history which contains duplicates of certain words")
print( "    Moving from the end to the history to the last occurrence of 'new'...") 
keys = input_history.go_phrase("new", 'end')
print( "        Should move to the left until we have reached the word new", keys[0] == "left:40")
print( "    Searching for 'sentence'...")
keys = input_history.go_phrase("sentence", 'end')
print( "        Should go left until the first occurrence of sentence, because it comes before the current cursor", keys[0] == "left:19")
print( "    Repeating the search for 'sentence' again...")
keys = input_history.go_phrase("sentence", 'end')
print( "        Should loop back to the last occurrence", keys[0] == "right:59")

input_history = get_filled_ihm()
print( "Using a filled input history which contains duplicates of certain words")
print( "    Moving from the end to the history to the last occurrence of 'to'...") 
keys = input_history.go_phrase("to", 'end')
print( "        Should move to the left until we have reached the word 'to'", keys[0] == "left:22")
print( "    Repeating the search for 'to' again...")
keys = input_history.go_phrase("to", 'end')
print( "        Should not move the cursor as there is only one option", len(keys) == 0)

input_history = get_filled_ihm()
print( "Using a filled input history which contains duplicates of certain words")
print( "    Moving from the end to the history to selecting the first occurrence of 'new'...") 
keys = input_history.select_phrase("new")
print( "        Should move to the left until we have reached the word 'new'", keys[0] == "left:44")
print( "        Should move to the right until we have reached the end of the word 'new'", keys[2] == "right:4")
print( "    Repeating the search for 'new' again...")
keys = input_history.select_phrase("new")
print( "        Should move to the left until we have reached the second occurrence", keys[1] == "left:29", keys)
print( "        Should move to the right until we have reached the end of the word 'new'", keys[3] == "right:4")