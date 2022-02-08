from collections import defaultdict
from typing import Mapping

from common.agent.agents.interaction_texts import markup_text, localize
from common.chat.language_enum import Language
from common.chat.localization_enum_mixin import PrettyLocalizationEnumMixin
from common.chat.platform.types import ChatPlatform
from common.utils.enums import EnumValueType
from echo.common.agent.agents.interaction_texts import (
    NAME_TEXT_NOT_LOCALIZED, LANGUAGE_TEXT_NOT_LOCALIZED, WHERE_WE_SAVE_YOUR_DATA_TEXT_NOT_LOCALIZED,
    FOR_WHICH_PURPOSE_WE_SAVE_YOUR_DATA_TEXT_NOT_LOCALIZED, WHICH_AGENT_BEHAVIOUR_USE_YOUR_DATA_TEXT_NOT_LOCALIZED,
    WHO_CAN_ACCESS_YOUR_DATA_TEXT_NOT_LOCALIZED, YOUR_DATA_IS_STORED_IN_TEXT_NOT_LOCALIZED
)


class SavedUserData(PrettyLocalizationEnumMixin):
    """Enum containing all user saved data description"""

    NAME = 'First Name'
    LANGUAGE = 'Language'
    TELEGRAM_ID = 'Telegram ID'
    PRYV_API_TOKEN = 'Pryv API Token'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.NAME.value: NAME_TEXT_NOT_LOCALIZED,
            cls.LANGUAGE.value: LANGUAGE_TEXT_NOT_LOCALIZED,
            cls.TELEGRAM_ID.value: {
                Language.LANGUAGE_ENGLISH: 'Telegram ID',
                Language.LANGUAGE_ITALIAN: 'ID Telegram',
                Language.LANGUAGE_FRENCH: 'ID Telegram',
                Language.LANGUAGE_GERMAN: 'Telegram ID',
            },
            cls.PRYV_API_TOKEN.value: {
                Language.LANGUAGE_ENGLISH: 'The Pryv access Token',
                Language.LANGUAGE_ITALIAN: 'Il token di accesso a Pryv',
                Language.LANGUAGE_FRENCH: 'Le jeton d\'accès Pryv',
                Language.LANGUAGE_GERMAN: 'Das Pryv-Zugriffstoken',
            },
        }


class Storage(PrettyLocalizationEnumMixin):
    """Enum containing type of storage used in project"""

    MONGO_DB = 'MongoDB'
    PRYV = 'Pryv'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.MONGO_DB.value: {
                Language.LANGUAGE_ENGLISH: 'MongoDB',
                Language.LANGUAGE_ITALIAN: 'MongoDB',
                Language.LANGUAGE_FRENCH: 'MongoDB',
                Language.LANGUAGE_GERMAN: 'MongoDB',
            },
            cls.PRYV.value: {
                Language.LANGUAGE_ENGLISH: 'Pryv',
                Language.LANGUAGE_ITALIAN: 'Pryv',
                Language.LANGUAGE_FRENCH: 'Pryv',
                Language.LANGUAGE_GERMAN: 'Pryv',
            },
        }


class StorageLocation(PrettyLocalizationEnumMixin):
    """Enum containing where the data is stored"""

    SWITZERLAND = 'Switzerland'
    PRYV_SELECTED = 'Pryv selected'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[EnumValueType, Mapping[Language, str]]:
        return {
            cls.SWITZERLAND.value: {
                Language.LANGUAGE_ENGLISH: 'Switzerland',
                Language.LANGUAGE_ITALIAN: 'Svizzera',
                Language.LANGUAGE_FRENCH: 'Suisse',
                Language.LANGUAGE_GERMAN: 'Schweiz',
            },
            cls.PRYV_SELECTED.value: {
                Language.LANGUAGE_ENGLISH: 'Location decided on Pryv',
                Language.LANGUAGE_ITALIAN: 'Locazione decisa su Pryv',
                Language.LANGUAGE_FRENCH: 'Emplacement décidé sur Pryv',
                Language.LANGUAGE_GERMAN: 'Standort auf Pryv entschieden',
            },
        }


class Purpose(PrettyLocalizationEnumMixin):
    """Enum containing purposes for which the data is saved"""

    TO_MONITOR = 'To monitor'
    TO_SUGGEST = 'To make suggestions'
    TO_CONTACT = 'To contact'
    TO_PROFILE = 'To profile'
    TO_MANAGE_DATA = 'To manage data'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.TO_MONITOR.value: {
                Language.LANGUAGE_ENGLISH: 'To monitor',
                Language.LANGUAGE_ITALIAN: 'Per monitorare',
                Language.LANGUAGE_FRENCH: 'Surveiller',
                Language.LANGUAGE_GERMAN: 'Zu überwachen',
            },
            cls.TO_SUGGEST.value: {
                Language.LANGUAGE_ENGLISH: 'To make suggestions',
                Language.LANGUAGE_ITALIAN: 'Per darti suggerimenti',
                Language.LANGUAGE_FRENCH: 'Pour faire des suggestions',
                Language.LANGUAGE_GERMAN: 'Vorschläge machen',
            },
            cls.TO_CONTACT.value: {
                Language.LANGUAGE_ENGLISH: 'To contact you',
                Language.LANGUAGE_ITALIAN: 'Per contattarti',
                Language.LANGUAGE_FRENCH: 'Te contacter',
                Language.LANGUAGE_GERMAN: 'Dich kontaktieren',
            },
            cls.TO_PROFILE.value: {
                Language.LANGUAGE_ENGLISH: 'To profile you',
                Language.LANGUAGE_ITALIAN: 'Per profilarti',
                Language.LANGUAGE_FRENCH: 'Pour vous profiler',
                Language.LANGUAGE_GERMAN: 'Um dich zu profilieren',
            },
            cls.TO_MANAGE_DATA.value: {
                Language.LANGUAGE_ENGLISH: 'To manage data',
                Language.LANGUAGE_ITALIAN: 'Per gestire i dati',
                Language.LANGUAGE_FRENCH: 'Pour gérer les données',
                Language.LANGUAGE_GERMAN: 'Daten verwalten',
            },
        }


class WhoHasAccess(PrettyLocalizationEnumMixin):
    """Enum containing who can access the data stored"""

    NO_HUMAN = "No Human"
    ONLY_SYS_ADMIN = "Admin"
    ADMIN_AND_DOCTOR = "Admin and Doctor"
    EVERYONE = "Everyone"

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[str, Mapping[Language, str]]:
        return {
            cls.NO_HUMAN.value: {
                Language.LANGUAGE_ENGLISH: 'No Human',
                Language.LANGUAGE_ITALIAN: 'Nessun umano',
                Language.LANGUAGE_FRENCH: 'Pas d\'humain',
                Language.LANGUAGE_GERMAN: 'Kein Mensch',
            },
            cls.ONLY_SYS_ADMIN.value: {
                Language.LANGUAGE_ENGLISH: 'Only System Administrator',
                Language.LANGUAGE_ITALIAN: 'Solo l\'amministratore del sistema',
                Language.LANGUAGE_FRENCH: 'Seul l\'administrateur système',
                Language.LANGUAGE_GERMAN: 'Nur der Systemadministrator',
            },
            cls.ADMIN_AND_DOCTOR.value: {
                Language.LANGUAGE_ENGLISH: 'System Admin and Doctor',
                Language.LANGUAGE_ITALIAN: 'L\'amministratore del sistema e il dottore',
                Language.LANGUAGE_FRENCH: 'L\'administrateur système et le médecin',
                Language.LANGUAGE_GERMAN: 'Der Systemadministrator und der Arzt',
            },
            cls.EVERYONE.value: {
                Language.LANGUAGE_ENGLISH: 'Everyone',
                Language.LANGUAGE_ITALIAN: 'Tutti',
                Language.LANGUAGE_FRENCH: 'Tous',
                Language.LANGUAGE_GERMAN: 'Alles',
            },
        }


class AgentBehaviours(PrettyLocalizationEnumMixin):
    """Enum containing which agent behaviours have access to user data"""

    REGISTRATION_BEHAVIOURS = 'Registration behaviours'
    ECHO_BEHAVIOURS = 'Echo behaviours'

    @classmethod
    def values_prettifier_not_localized(cls) -> Mapping[EnumValueType, Mapping[Language, str]]:
        return {
            cls.REGISTRATION_BEHAVIOURS.value: {
                Language.LANGUAGE_ENGLISH: 'Registration behaviours',
                Language.LANGUAGE_ITALIAN: 'Behaviours di registrazione',
                Language.LANGUAGE_FRENCH: 'Behaviours pour l\'inscription',
                Language.LANGUAGE_GERMAN: 'Behaviours für die Registrierung',
            },
            cls.ECHO_BEHAVIOURS.value: {
                Language.LANGUAGE_ENGLISH: 'Echo behaviours',
                Language.LANGUAGE_ITALIAN: 'Behaviours per la funzione eco',
                Language.LANGUAGE_FRENCH: 'Behaviours de la fonction écho',
                Language.LANGUAGE_GERMAN: 'Behaviours für die Echo-Funktion',
            },
        }


DATA_TO_STORAGE = {
    SavedUserData.NAME: [Storage.PRYV],
    SavedUserData.LANGUAGE: [Storage.PRYV],
    SavedUserData.TELEGRAM_ID: [Storage.MONGO_DB],
    SavedUserData.PRYV_API_TOKEN: [Storage.MONGO_DB],
}

DATA_TO_PURPOSE = {
    SavedUserData.NAME: [Purpose.TO_PROFILE, Purpose.TO_CONTACT],
    SavedUserData.LANGUAGE: [Purpose.TO_PROFILE, Purpose.TO_CONTACT],
    SavedUserData.TELEGRAM_ID: [Purpose.TO_CONTACT],
    SavedUserData.PRYV_API_TOKEN: [Purpose.TO_MANAGE_DATA],
}

DATA_TO_ACCESS = {
    SavedUserData.NAME: [WhoHasAccess.ADMIN_AND_DOCTOR],
    SavedUserData.LANGUAGE: [WhoHasAccess.ADMIN_AND_DOCTOR],
    SavedUserData.TELEGRAM_ID: [WhoHasAccess.ONLY_SYS_ADMIN],
    SavedUserData.PRYV_API_TOKEN: [WhoHasAccess.ONLY_SYS_ADMIN],
}

DATA_TO_AGENT_BEHAVIOURS = {
    SavedUserData.NAME: [AgentBehaviours.REGISTRATION_BEHAVIOURS],
    SavedUserData.LANGUAGE: [AgentBehaviours.REGISTRATION_BEHAVIOURS],
    SavedUserData.TELEGRAM_ID: [
        AgentBehaviours.REGISTRATION_BEHAVIOURS,
        AgentBehaviours.ECHO_BEHAVIOURS,
    ],
    SavedUserData.PRYV_API_TOKEN: [
        AgentBehaviours.REGISTRATION_BEHAVIOURS,
        AgentBehaviours.ECHO_BEHAVIOURS,
    ],
}


def generate_privacy_statement_not_localized(platform_type: ChatPlatform) -> Mapping[Language, str]:
    """Method to generate the privacy statement not localized"""

    paragraphs = [
        (WHERE_WE_SAVE_YOUR_DATA_TEXT_NOT_LOCALIZED, Storage),
        (FOR_WHICH_PURPOSE_WE_SAVE_YOUR_DATA_TEXT_NOT_LOCALIZED, Purpose),
        (WHO_CAN_ACCESS_YOUR_DATA_TEXT_NOT_LOCALIZED, WhoHasAccess),
        (WHICH_AGENT_BEHAVIOUR_USE_YOUR_DATA_TEXT_NOT_LOCALIZED, AgentBehaviours)
    ]

    output_privacy_statement = defaultdict(lambda: "")

    for index, (paragraph_title_not_localized, enum_class) in enumerate(paragraphs):
        current_assignment_mapping = (
            DATA_TO_STORAGE if enum_class == Storage
            else DATA_TO_PURPOSE if enum_class == Purpose
            else DATA_TO_ACCESS if enum_class == WhoHasAccess
            else DATA_TO_AGENT_BEHAVIOURS
        )
        for language, paragraph_title in paragraph_title_not_localized.items():
            output_privacy_statement[language] = (
                f"{output_privacy_statement[language]}"
                f"{index + 1}. {markup_text(paragraph_title, bold=True)}\n\n"
            )
            if paragraph_title_not_localized == WHERE_WE_SAVE_YOUR_DATA_TEXT_NOT_LOCALIZED:
                output_privacy_statement[language] = (
                    f"{output_privacy_statement[language]}"
                    f"{localize(YOUR_DATA_IS_STORED_IN_TEXT_NOT_LOCALIZED, language)}"
                    f"{StorageLocation.pretty_values_localized(language)}\n\n"
                )

            for user_data in SavedUserData:
                if user_data == SavedUserData.TELEGRAM_ID and platform_type != ChatPlatform.TELEGRAM:
                    continue
                pretty_user_data = SavedUserData.values_prettifier_localized(language)[user_data.value]
                pretty_specification = [
                    enum_class.values_prettifier_localized(language)[elem.value]
                    for elem in current_assignment_mapping[user_data]
                ]
                output_privacy_statement[language] = (
                    f"{output_privacy_statement[language]}"
                    f"{markup_text(pretty_user_data, bold=True)}:  "
                    f"{pretty_specification}\n"
                )

            output_privacy_statement[language] = f"{output_privacy_statement[language]}\n\n\n"

    return output_privacy_statement

