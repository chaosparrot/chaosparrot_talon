from talon import Module, Context, actions, settings, ui
from .input_history import InputHistoryManager
from typing import List
from .formatters.formatters import FORMATTERS_LIST
from .formatters.text_formatter import TextFormatter

mod = Module()

mod.setting("context_remove_undo", type=str, default="ctrl-z", desc="The key combination to undo a paste action")
mod.setting("context_remove_word", type=str, default="ctrl-backspace", desc="The key combination to clear a word to the left of the cursor")
mod.setting("context_remove_letter", type=str, default="backspace", desc="The key combination to clear a single letter to the left of the cursor")
mod.setting("context_remove_forward_word", type=str, default="ctrl-delete", desc="The key combination to clear a word to the right of the cursor")
mod.setting("context_remove_forward_letter", type=str, default="delete", desc="The key combination to clear a single letter to the right of the cursor")

mod.tag("flow_numbers", desc="Ensure that the user can freely insert numbers")
mod.tag("flow_letters", desc="Ensure that the user can freely insert letters")
mod.tag("flow_symbols", desc="Ensure that the user can freely insert symbols")
mod.tag("flow_words", desc="Ensure that the user can freely insert words")

mod.tag("context_disable_shift_selection", desc="Disables shift selection for the current context")
mod.tag("context_disable_word_wrap", desc="Disables word wrap detection for the current context")
mod.tag("context_disable_word_wrap", desc="Disables word wrap detection for the current context")

mod.list("input_history_words", desc="A list of words that correspond to inserted text and their cursor positions for quick navigation in text")
ctx = Context()
ctx.lists["user.input_history_words"] = []

# Class to manage all the talon bindings and key presses for input history
class InputMutator:
    manager: InputHistoryManager
    active_formatters: List[TextFormatter]
    formatters_name: List[str]
    tracking = True

    insert_application_id: int = 0
    current_application_pid: int = 0

    def __init__(self):
        self.manager = InputHistoryManager()
        self.active_formatters = []
        self.formatters_name = []

    def set_formatter(self, name: str):
        if name in FORMATTERS_LIST:
            self.active_formatters = [FORMATTERS_LIST[name]]
            self.formatters_name = [name]

    def enable_tracking(self):
        self.tracking = True

    def disable_tracking(self):
        self.tracking = False

    def track_key(self, key_string: str):
        if self.tracking:
            keys = key_string.replace(":up", "").replace(":down", "").replace(":", "").split(" ")            
            if self.insert_application_id != self.current_application_pid:
                actions.user.hud_add_log("error", "Clear because application id is off", self.insert_application_id)
                self.insert_application_id = self.current_application_pid
                self.formatters = []
                self.manager.clear_input_history()
            
            self.manager.apply_key(key_string)
            self.index()

    def track_insert(self, insert: str, phrase: str = None):
        if self.tracking:
            if self.insert_application_id != self.current_application_pid:
                actions.user.hud_add_log("error", "Clear because application id is off")
                self.insert_application_id = self.current_application_pid
                self.formatters = []
                self.manager.clear_input_history()

            input_events = []

            # Automatic insert splitting if no explicit phrase is given
            if phrase == "" and " " in insert:
                inserts = insert.split(" ")
                for index, text in enumerate(inserts):
                    if index < len(inserts) - 1:
                        text += " "
                    input_events.extend(self.manager.text_to_input_history_events(text, None, "|".join(self.formatters_name)))
            else:
                input_events = self.manager.text_to_input_history_events(insert, phrase, "|".join(self.formatters_name))
            self.manager.insert_input_events(input_events)
            self.index()

    def is_selecting(self) -> bool:
        return self.manager.is_selecting()

    def has_phrase(self, phrase: str) -> bool:
        for event in self.manager.input_history:
            if event.phrase.lower() == phrase.lower():
                return True
            
        return False
    
    def move_cursor_back(self) -> List[str]:
        if len(self.manager.input_history) > 0:
            last_event = self.manager.input_history[-1]
            return self.manager.navigate_to_event(last_event, -1, False)
        else:
            return ["end"]

    def move_to_phrase(self, phrase: str, character_index: int = -1, keep_selection: bool = False, next_occurrence: bool = True) -> List[str]:
        return self.manager.go_phrase(phrase, "end" if character_index == -1 else "start", keep_selection, next_occurrence )

    def transform_insert(self, insert: str) -> str:
        if not self.active_formatters:
            return insert
        else:
            return "".join(self.active_formatters[0].words_to_format(insert.split()))

    def clear_keys(self, backwards = True) -> List[str]:
        context = self.manager.determine_context()

        if self.is_selecting():
            return [settings.get("user.context_remove_letter")]
        
        if context.current is not None:
            if context.character_index == 0 and backwards and context.previous is not None:
                return [settings.get("user.context_remove_letter") + ":" + str(len(context.previous.text))]

            elif context.character_index == len(context.current.text):
                if not backwards and context.next is not None:
                    return [settings.get("user.context_remove_forward_letter") + ":" + str(len(context.next.text))]
                elif backwards:
                    return [settings.get("user.context_remove_letter") + ":" + str(len(context.current.text))]

            if context.character_index > 0 and context.character_index < len(context.current.text) - 1:
                if backwards:
                    return [settings.get("user.context_remove_letter") + ":" + str(context.character_index)]
                else:
                    return [settings.get("user.context_remove_forward_letter") + ":" + str(len(context.current.text) - context.character_index)]

        return [settings.get("user.context_remove_word") if backwards else settings.get("user.context_remove_forward_word")]

    def index(self):
        words_list = []
        for event in self.manager.input_history:
            words_list.append(event.phrase)
        ctx.lists["user.input_history_words"] = words_list

        tags = []
        input_index = self.manager.determine_input_index()
        if input_index[0] > -1 and input_index[1] > -1:
            event = self.manager.input_history[input_index[0]]
            # TODO APPLY FLOW TAGS DEPENDING ON WORDS
        ctx.tags = tags

    def focus_changed(self, event):
        self.current_application_pid = event.app.pid if event.app else -1

mutator = InputMutator()
ui.register("win_focus", mutator.focus_changed)


@mod.action_class
class Actions:

    def input_core_enable_tracking():
        """Enable tracking of input values so that we can make contextual decisions and keep the cursor position"""
        global mutator
        mutator.enable_tracking()

    def input_core_disable_tracking():
        """Disable tracking of input values"""
        global mutator
        mutator.disable_tracking()

    def input_core_set_formatter(formatter: str):
        """Sets the current formatter to be used in text editing"""
        global mutator
        mutator.set_formatter(formatter)

    def input_core_transform_insert(insert: str) -> str:
        """Transform an insert automatically depending on previous context"""
        global mutator
        return mutator.transform_insert(insert)

    def input_core_insert(prose: str):
        """Input words based on context surrounding the words to input"""
        global mutator
        actions.insert(actions.user.input_core_transform_insert(prose))

    def input_core_track_key(key_string: str) -> str:
        """Track one or more key presses according to the key string"""
        global mutator
        mutator.track_key(key_string)

    def input_core_track_insert(insert: str, phrase: str = "") -> str:
        """Track a full insert"""
        global mutator
        mutator.track_insert(insert, phrase)

    def input_core_clear(backward: bool = True):
        """Apply a clear based on the current input history"""
        global mutator
        keys = mutator.clear_keys(backward)        
        actions.user.hud_add_log("warning", "CLEAR! " + " ".join(keys))
        for key in keys:
            actions.key(key)

    def input_core_move_cursor(phrase: str, cursor_position: int = -1):
        """Move the cursor to the given phrase"""
        global mutator
        if mutator.has_phrase(phrase):
            keys = mutator.move_to_phrase(phrase, cursor_position)
            if keys:
                mutator.disable_tracking()
                for key in keys:
                    actions.key(key)
                mutator.enable_tracking()
        else:
            actions.user.hud_add_log("command", phrase + " could not be found in context")
            raise RuntimeError("Input phrase '" + phrase + "' could not be found in the history")

    def input_core_select(phrase: str):
        """Move the cursor to the given phrase and select it"""
        global mutator

        if mutator.has_phrase(phrase):
            before_keys = mutator.move_to_phrase(phrase, 0, False, True)
            mutator.disable_tracking()
            if before_keys:
                for key in before_keys:
                    actions.key(key)
            mutator.enable_tracking()

            actions.key("shift:down")
            mutator.disable_tracking()
            after_keys = mutator.move_to_phrase(phrase, -1, True, False)
            if after_keys:
                for key in after_keys:
                    actions.key(key)
            mutator.enable_tracking()
            actions.key("shift:up")            
        else:
            actions.user.hud_add_log("warning", phrase + " could not be found in context")
            raise RuntimeError("Input phrase '" + phrase + "' could not be found in the history")

    def input_core_clear_phrase(phrase: str):
        """Move the cursor behind the given phrase and remove it"""
        global mutator
        before_keys = mutator.move_to_phrase(phrase, -1, False, False)
        mutator.disable_tracking()
        if before_keys:
            for key in before_keys:
                actions.key(key)
        mutator.enable_tracking()

        keys = mutator.clear_keys()
        actions.user.hud_add_log("warning", "CLEAR! " + " ".join(keys))
        for key in keys:
            actions.key(key)

    def input_core_continue():
        """Move the cursor to the end of the current input history"""
        global mutator
        keys = mutator.move_cursor_back()

        mutator.disable_tracking()
        for key in keys:
            actions.key(key)
        mutator.enable_tracking()

    def input_core_print():
        """Print the current input core state"""
        global mutator
        print( "Input state")
        print( "----------" )
        print( mutator.manager.cursor_position_tracker.text_history )
        print( "----------" )