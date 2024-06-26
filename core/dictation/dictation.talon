mode: dictation
-
<user.raw_prose>: user.virtual_buffer_self_repair_insert(raw_prose)
^quill <user.word>$:
    user.virtual_buffer_insert(word)
^quill <user.word> <user.raw_prose>:
    user.virtual_buffer_insert(word)
    user.virtual_buffer_insert(raw_prose)

^cursor before {user.indexed_words} [quill]:
    user.virtual_buffer_move_caret(indexed_words, 0)

^cursor after {user.indexed_words} [quill]:
    user.virtual_buffer_move_caret(indexed_words, -1)

# Spelling
^<user.direct_spelling>:
    user.virtual_buffer_insert(direct_spelling)