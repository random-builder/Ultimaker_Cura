
import os
import re
import unittest
import pytest

MSGCTXT = "msgctxt" # Scope of the text
MSGID =  "msgid" # The id of the text, also English version
MSGTR = "msgstr" # The translation

regex_patter = '(&[\w])' #"&[a-zA-Z0-9]" - Search char '&' and at least one character after it, the '+' returns one char after '&'


# class TestShortcutKeys(unittest.TestCase):
#
#     language_folder = [
#         "en_7S",
#         "de_DE",
#         "en_US",
#         "es_ES",
#         "fi_FI",
#         "fr_FR",
#         "hu_HU",
#         "it_IT",
#         "ja_JP",
#         "ko_KR",
#         "nl_NL",
#         "pl_PL",
#         "pt_BR",
#         "ru_RU",
#         "tr_TR"
#     ]

@pytest.mark.parametrize("language_type", [("en_7S"),("de_DE"),("es_ES"),("fi_FI"),("fr_FR"),("hu_HU")])
def test_shortcut_keys(language_type):

    language_folder = language_type

    translation_file_name = "cura.po"

    plugin_file_path = os.path.dirname(os.path.abspath(__file__))
    path_records = os.path.split(plugin_file_path)
    global_path = path_records[:-1]
    cura_path = os.path.join(*global_path)
    language_file_path = os.path.join(cura_path,"resources","i18n",language_folder, translation_file_name)


    last_translation_scope = ""
    last_translation_id = ""
    last_translation_text = ""

    #{shortcut_key, {scope, [translation_text]}}
    shortcut_keys = dict()
    with open(language_file_path,'r') as f:
        for text in f:

            if text.startswith(MSGCTXT):
                last_translation_scope = text
            elif text.startswith(MSGID):
                last_translation_id = text
            elif text.startswith(MSGTR):
                last_translation_text = text

                #if text has '&'symbol and at least one character (char or digit) should be after it
                # ex '&acr mytest' -> this should return '&a'
                the_shortcut_key_word = re.search(regex_patter, text)

                if the_shortcut_key_word is not None:
                    # take only char after '&' symbol
                    the_shortcut_key = the_shortcut_key_word.group(0)[1]

                    the_shortcut_key = the_shortcut_key.upper() #make all shortcut keys capital

                    #The shortcut key is not yet added
                    if the_shortcut_key not in shortcut_keys:
                        scope_translation = dict()
                        scope_translation[last_translation_scope] = []
                        scope_translation[last_translation_scope].append(text)

                        shortcut_keys[the_shortcut_key] = scope_translation
                    else:
                        #check if the shortcut key scope is already added
                        if last_translation_scope not in shortcut_keys[the_shortcut_key]:
                            scope_translation = dict()
                            scope_translation[last_translation_scope] = []
                            scope_translation[last_translation_scope].append(text)
                            shortcut_keys[the_shortcut_key].update(scope_translation)

                            # if the scope already exist then add the key
                        elif last_translation_scope in shortcut_keys[the_shortcut_key]:
                            shortcut_keys[the_shortcut_key][last_translation_scope].append(text)


                last_translation_scope = ""
                last_translation_id = ""

    not_valid_shortcut_keys = []
    #Validate all shortcut keys
    for shortcut_key, scopes in shortcut_keys.items():

        #check, whether the exist in one scope multiple times or not
        for key, items in scopes.items():

            if len (items) > 1:
                not_valid_shortcut_keys.append(items)

    if len(not_valid_shortcut_keys) != 0:
        temp='%s' % ', '.join(map(str, not_valid_shortcut_keys))
        print("NOT VALID KEYS: " + temp)


    assert len(not_valid_shortcut_keys) == 0


if __name__ == "__main__":
    suite = unittest.TestSuite()


    unittest.main(suite)