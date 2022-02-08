from typing import Collection


class KeyboardObjectFactory:
    """A factory for keyboard objects consumed by the CustomChat platform"""

    class Fields:
        KEYBOARD_FIELD = "keyboard"
        QUICK_REPLY_KEYBOARD_FIELD = "quick_reply_keyboard"
        REMOVE_CUSTOM_KEYBOARD_FIELD = "remove_custom_keyboard"
        OPTION_TEXT = "option_text"

    @staticmethod
    def _distribute_options(options: Collection[str], row_width: int):
        """
        Utility method to refactor the logic of creating keyboard arrays of arrays.
        These arrays will represent keyboards as matrices
        """
        temp_keyboard_array = []
        for index, option in enumerate(options):
            if index % row_width == 0:
                temp_keyboard_array.append([])

            temp_keyboard_array[-1].append({
                KeyboardObjectFactory.Fields.OPTION_TEXT: option
            })

        return temp_keyboard_array

    @staticmethod
    def create_menu_object(options: Collection[str], row_width: int):
        """Creates a menu object to be sent to the client for rendering"""

        return {
            KeyboardObjectFactory.Fields.KEYBOARD_FIELD: KeyboardObjectFactory._distribute_options(options, row_width)
        }

    @staticmethod
    def create_quick_replies_object(options: Collection[str], row_width: int = 4):
        """Creates the quick replies object to be sent for rendering to the client"""

        return {
            KeyboardObjectFactory.Fields.QUICK_REPLY_KEYBOARD_FIELD:
                KeyboardObjectFactory._distribute_options(options, row_width)
        }

    @staticmethod
    def create_show_normal_keyboard_object() -> dict:
        """Creates a menu object which hides the custom keyboard in client rendering, showing the normal one"""
        return {KeyboardObjectFactory.Fields.REMOVE_CUSTOM_KEYBOARD_FIELD: True}
