from typing import Mapping, Optional, Collection, List

from common.chat.language_enum import Language


def markup_text(text: str, bold: bool = False, italic: bool = False) -> str:
    """Utility function to markup text in MARKDOWN"""

    starting = ""
    ending = ""

    if bold:
        starting = f"*{starting}"
        ending = f"{ending}*"

    if italic:
        starting = f"_{starting}"
        ending = f"{ending}_"

    return f"{starting}{text}{ending}"


def localize(to_localize: Mapping[Language, str], language: Optional[Language]) -> str:
    """A method to localize messages, defaulting to english if not localized"""

    return to_localize.get(language, to_localize[Language.LANGUAGE_ENGLISH])


def localize_list(to_localize: Collection[Mapping[Language, str]], language: Optional[Language]) -> List[str]:
    """A utility method to apply localization over a list of to localize objects"""

    return [localize(not_localized, language) for not_localized in to_localize]


HELLO_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Hello",
    Language.LANGUAGE_ITALIAN: "Ciao",
    Language.LANGUAGE_FRENCH: "Bonjour",
    Language.LANGUAGE_GERMAN: "Hallo",
}

NOT_FOUND_DOCTOR_AGENT_USER_MESSAGE_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: (
        "Sorry for the inconvenience. The system is not ready to process your request.\n"
        "Try again soon. 😇"
    ),
    Language.LANGUAGE_ITALIAN: (
        "Ci scusiamo per l'inconveniente. Il sistema non è pronto per elaborare la tua richiesta.\n"
        "Riprova presto. 😇"
    ),
    Language.LANGUAGE_FRENCH: (
        "Désolé pour la gêne occasionnée. Le système n'est pas prêt à traiter votre demande.\n"
        "Réessaye bientôt. 😇"
    ),
    Language.LANGUAGE_GERMAN: (
        "Entschuldigen Sie die Unannehmlichkeiten. Das System ist nicht bereit, Ihre Anfrage zu bearbeiten.\n"
        "Versuchen Sie es bald noch einmal. 😇"
    ),
}

SORRY_INTERNAL_ERROR_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: (
        "Sorry for the inconvenience. "
        "The system encountered an error, we will fix this in short hopefully.\n"

        "Try again soon. 😇"
    ),
    Language.LANGUAGE_ITALIAN: (
        "Ci scusiamo per l'inconveniente. "
        "Il sistema ha riscontrato un errore, speriamo di risolverlo in breve.\n"

        "Riprova presto. 😇"
    ),
    Language.LANGUAGE_FRENCH: (
        "Désolé pour la gêne occasionnée. "
        "Le système a rencontré une erreur, nous allons résoudre ce problème en bref, espérons-le.\n"

        "Réessaye bientôt. 😇"
    ),
    Language.LANGUAGE_GERMAN: (
        "Entschuldigen Sie die Unannehmlichkeiten. "
        "Das System hat einen Fehler festgestellt. "
        "Wir werden diesen hoffentlich kurz beheben.\n"

        "Versuchen Sie es bald noch einmal. 😇"
    ),
}

NOT_A_VALID_RESPONSE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "It's not a valid answer.",
    Language.LANGUAGE_ITALIAN: "Non è una risposta valida.",
    Language.LANGUAGE_FRENCH: "Ce n'est pas une réponse valable.",
    Language.LANGUAGE_GERMAN: "Es ist keine gültige Antwort.",
}

SELECT_ONE_OF_THE_OPTIONS_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Select one of the options below.",
    Language.LANGUAGE_ITALIAN: "Seleziona una delle opzioni sotto.",
    Language.LANGUAGE_FRENCH: "Sélectionnez l'une des options ci-dessous.",
    Language.LANGUAGE_GERMAN: "Wähle eine der folgenden Optionen.",
}

LETS_COMPLETE_YOUR_PROFILE_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Let's complete your profile information :memo:",
    Language.LANGUAGE_ITALIAN: "Completa le informazioni del tuo profilo :memo:",
    Language.LANGUAGE_FRENCH: "Complétons les informations de votre profil :memo:",
    Language.LANGUAGE_GERMAN: "Vervollständigen wir Ihre Profilinformationen :memo:",
}

I_DONT_UNDERSTAND_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "I don't understand :thinking_face:",
    Language.LANGUAGE_ITALIAN: "Non ho capito :thinking_face:",
    Language.LANGUAGE_FRENCH: "Je ne comprends pas :thinking_face:",
    Language.LANGUAGE_GERMAN: "Ich verstehe nicht :thinking_face:",
}
