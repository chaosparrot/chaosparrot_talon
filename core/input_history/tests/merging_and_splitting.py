from ..cursor_position_tracker import _CURSOR_MARKER
from ..input_indexer import text_to_input_history_events
from ..input_history import InputHistoryManager
from ...utils.test import create_test_suite

def test_merging_and_splitting(assertion):
    input_history = InputHistoryManager() 
    input_history.insert_input_events(text_to_input_history_events("Insert a new sentence. \n", "insert a new sentence"))
    input_history.insert_input_events(text_to_input_history_events("Insert a second sentence. \n", "insert a second sentence"))
    input_history.insert_input_events(text_to_input_history_events("Insert a third sentence.", "insert a third sentence"))
    input_history.cursor_position_tracker.text_history = """Insert a new sentence.
Insert a second """ + _CURSOR_MARKER + """sentence. 
Insert a third sentence."""
        
    assertion( "    Inserting unmergable text into a filled input history...")
    input_history.insert_input_events(text_to_input_history_events("important ", "important")) 
    assertion( "        Expect history length to increase by two (5)", len(input_history.input_history) == 5)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the same as before (10)", cursor_index[1] == 10)
    input_index = input_history.determine_input_index()
    assertion( "        Expect input index to be at the inserted event", input_index[0] == 2)
    assertion( "        Expect input character index to be the length of the inserted event (10)", input_index[1] == 10 )     
    assertion( "        Expect the previous event text to be split into a before section", input_history.input_history[1].text == "Insert a second " )
    assertion( "        Expect the previous event phrase to be split into a before section", input_history.input_history[1].phrase == "insert a second" )
    assertion( "        Expect the previous event text to be split into an after section", input_history.input_history[3].text == "sentence. \n" )
    assertion( "        Expect the previous event phrase to be split into an after section", input_history.input_history[3].phrase == "sentence" )
    assertion( "    Inserting mergable text...")
    input_history.insert_input_events(text_to_input_history_events("end", "end")) 
    assertion( "        Expect history length to not increase (5)", len(input_history.input_history) == 5)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the same as before (10)", cursor_index[1] == 10)
    input_index = input_history.determine_input_index()
    assertion( "        Expect input index to be at the merged event", input_index[0] == 3)
    assertion( "        Expect input character index to be the third character of the merged event (3)", input_index[1] == 3 )
    assertion( "        Expect the next event text to be merged", input_history.input_history[3].text == "endsentence. \n" )
    assertion( "        Expect the next event phrase to be merged", input_history.input_history[3].phrase == "endsentence" )
    assertion( "    Inserting a mergable character...")    
    input_history.insert_input_events(text_to_input_history_events("i", "i")) 
    assertion( "        Expect history length to not increase (5)", len(input_history.input_history) == 5)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the same as before (10)", cursor_index[1] == 10)
    input_index = input_history.determine_input_index()
    assertion( "        Expect input index to be at the merged event", input_index[0] == 3)
    assertion( "        Expect input character index to be the third character of the merged event (4)", input_index[1] == 4 )
    assertion( "        Expect the current event text to be merged", input_history.input_history[3].text == "endisentence. \n" )
    assertion( "        Expect the current event phrase to be merged", input_history.input_history[3].phrase == "endisentence" )
    assertion( "    Inserting left-mergable text...")    
    input_history.insert_input_events(text_to_input_history_events("ng ", "ng")) 
    assertion( "        Expect history length to increase (6)", len(input_history.input_history) == 6)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the same as before (10)", cursor_index[1] == 10)
    input_index = input_history.determine_input_index()
    assertion( "        Expect input index to be at the end of the merged event", input_index[0] == 3)
    assertion( "        Expect input character index to be the end character of the merged event (7)", input_index[1] == 7 )
    assertion( "        Expect the previous event text to be merged", input_history.input_history[3].text == "ending " )
    assertion( "        Expect the previous event phrase to be merged", input_history.input_history[3].phrase == "ending" )
    assertion( "        Expect the next event text to be split from the previous event", input_history.input_history[4].text == "sentence. \n" )
    assertion( "        Expect the next event phrase to be split from the previous event", input_history.input_history[4].phrase == "sentence" )
    assertion( "    Inserting right-mergable text...")
    input_history.insert_input_events(text_to_input_history_events("of", "of"))
    input_history.insert_input_events(text_to_input_history_events(" the", "the")) 
    assertion( "        Expect history length to increase (7)", len(input_history.input_history) == 7)
    cursor_index = input_history.cursor_position_tracker.get_cursor_index()
    assertion( "        Expect cursor line index to be 1", cursor_index[0] == 1)
    assertion( "        Expect cursor character index to be the same as before (10)", cursor_index[1] == 10)
    input_index = input_history.determine_input_index()
    assertion( "        Expect input index to be at the merged event", input_index[0] == 5)
    assertion( "        Expect input character index to be the fourht character of the merged event (4)", input_index[1] == 4 )
    assertion( "        Expect the previous event text to be split from the event", input_history.input_history[4].text == "of" )
    assertion( "        Expect the previous event phrase to be split from the event", input_history.input_history[4].phrase == "of" )
    assertion( "        Expect the next event text to be merged with the given event", input_history.input_history[5].text == " thesentence. \n" )
    assertion( "        Expect the next event phrase to be merged with the given event", input_history.input_history[5].phrase == "thesentence" )

suite = create_test_suite("Inserting in between input events")
suite.add_test(test_merging_and_splitting)