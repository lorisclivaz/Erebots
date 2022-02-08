from enum import Enum
from typing import Mapping

from common.agent.agents.interaction_texts import localize
from common.chat.language_enum import Language
from common.chat.localization_enum_mixin import PrettyLocalizationEnumMixin


class SlashCommands(PrettyLocalizationEnumMixin, Enum):
    """The commands accepted by ChatBot"""

    START = "/start"
    MENU = "/menu"
    HELP = "/help"

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.START.value: {
                Language.LANGUAGE_ENGLISH: "Welcomes you and explains who am I",
                Language.LANGUAGE_ITALIAN: "Ti dà il benvenuto e spiega chi sono io",
                Language.LANGUAGE_FRENCH: "Vous souhaite la bienvenue et vous explique qui je suis",
                Language.LANGUAGE_GERMAN: "Begrüßt Sie und erklärt, wer ich bin",
            },
            cls.MENU.value: {
                Language.LANGUAGE_ENGLISH: "Show menu commands",
                Language.LANGUAGE_ITALIAN: "Mostra i comandi del menu",
                Language.LANGUAGE_FRENCH: "Afficher les commandes de menu",
                Language.LANGUAGE_GERMAN: "Menübefehle anzeigen",
            },
            cls.HELP.value: {
                Language.LANGUAGE_ENGLISH: "Shows this help message",
                Language.LANGUAGE_ITALIAN: "Mostra questo messaggio di aiuto",
                Language.LANGUAGE_FRENCH: "Affiche ce message d'aide",
                Language.LANGUAGE_GERMAN: "Zeigt diese Hilfemeldung an",
            },
        }

    @staticmethod
    def create_help_string_not_localized() -> Mapping[Language, str]:
        """Returns the help string for the available commands"""

        i_accept_these_commands_text_not_localized = {
            Language.LANGUAGE_ENGLISH: "I accept these commands",
            Language.LANGUAGE_ITALIAN: "Accetto questi comandi",
            Language.LANGUAGE_FRENCH: "J'accepte ces commandes",
            Language.LANGUAGE_GERMAN: "Ich akzeptiere diese Befehle",
        }

        return {
            language: (
                    f"{localize(i_accept_these_commands_text_not_localized, language)}:\n\n" +
                    "\n\n".join(
                        [
                            f"{cmd} - {localize(explanation_not_localized, language)}"
                            for cmd, explanation_not_localized
                            in SlashCommands.values_prettifier_not_localized().items()
                        ]
                    )
            )
            for language in Language
        }


class UserFunctionality(PrettyLocalizationEnumMixin, Enum):
    """The functionality offered by the ChatBot."""

    LETS_EXERCISE = 'LETS_EXERCISE'
    TREND = 'TREND'
    UPDATE_PERSONAL_DATA = 'UPDATE_PERSONAL_DATA'
    PRIVACY_STATEMENT = 'PRIVACY_STATEMENT'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.LETS_EXERCISE.value: {
                Language.LANGUAGE_ENGLISH: ":flexed_biceps: Let's exercise",
                Language.LANGUAGE_ITALIAN: ":flexed_biceps: Esercitiamoci",
                Language.LANGUAGE_FRENCH: ":flexed_biceps: Faisons de l'exercice",
                Language.LANGUAGE_GERMAN: ":flexed_biceps: Lass uns trainieren",
            },
            cls.TREND.value: {
                Language.LANGUAGE_ENGLISH: ":chart_increasing: My statistics",
                Language.LANGUAGE_ITALIAN: ":chart_increasing: Le mie statistiche",
                Language.LANGUAGE_FRENCH: ":chart_increasing: Mes statistiques",
                Language.LANGUAGE_GERMAN: ":chart_increasing: Meine Statistiken",
            },
            cls.UPDATE_PERSONAL_DATA.value: {
                Language.LANGUAGE_ENGLISH: ":memo: Update profile",
                Language.LANGUAGE_ITALIAN: ":memo: Aggiorna il profilo",
                Language.LANGUAGE_FRENCH: ":memo: Mettre à jour le profil",
                Language.LANGUAGE_GERMAN: ":memo: Profil aktualisieren",
            },
            cls.PRIVACY_STATEMENT.value: {
                Language.LANGUAGE_ENGLISH: ":locked: Privacy statement",
                Language.LANGUAGE_ITALIAN: ":locked: Informativa sulla Privacy",
                Language.LANGUAGE_FRENCH: ":locked: Déclaration de confidentialité",
                Language.LANGUAGE_GERMAN: ":locked: Datenschutzerklärung",
            },
        }
