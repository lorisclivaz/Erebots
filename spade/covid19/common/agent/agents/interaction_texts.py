from collections import defaultdict
from typing import Mapping

from common.agent.agents.interaction_texts import markup_text
from common.chat.language_enum import Language

NEW_USER_MESSAGE_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "It seems you're a new user!",
    Language.LANGUAGE_ITALIAN: "Sembra che tua sia un nuovo utente!",
    Language.LANGUAGE_FRENCH: "Il semble que vous soyez un nouvel utilisateur!",
    Language.LANGUAGE_GERMAN: "Sie scheinen ein neuer Benutzer zu sein!",
}

BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH:
        "I am PhysioBotvid19, the robot that can help you doing physical activity! :flexed_biceps:",
    Language.LANGUAGE_ITALIAN:
        "Sono PhysioBotvid19, il robot che può aiutarti a fare attività fisica! :flexed_biceps:",
    Language.LANGUAGE_FRENCH:
        "Je suis PhysioBotvid19, le robot qui peut vous aider à faire de l'activité physique! :flexed_biceps:",
    Language.LANGUAGE_GERMAN:
        "Ich bin PhysioBotvid19, der Roboter, der Ihnen bei körperlicher Aktivität helfen kann! :flexed_biceps:",
}

START_COMMAND_ALREADY_REGISTERED_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH:
        f"{BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED[Language.LANGUAGE_ENGLISH]}\n\n"

        "You can always access this menu by sending me the command /menu or you can see a description of "
        "the other commands which I support, by sending me /help. :smiling_face_with_smiling_eyes:",
    Language.LANGUAGE_ITALIAN:
        f"{BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED[Language.LANGUAGE_ITALIAN]}\n\n"

        "Puoi sempre accedere a questo menù inviandomi il comando /menu oppure puoi vedere una descrizione degli"
        " altri comandi che supporto, inviandomi /help. :smiling_face_with_smiling_eyes:",
    Language.LANGUAGE_FRENCH:
        f"{BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED[Language.LANGUAGE_FRENCH]}\n\n"

        "Vous pouvez toujours accéder à ce menu en m'envoyant la commande /menu ou vous pouvez voir une description des"
        " autres commandes que je supporte, en m'envoyant /help. :smiling_face_with_smiling_eyes:",
    Language.LANGUAGE_GERMAN:
        f"{BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED[Language.LANGUAGE_GERMAN]}\n\n"

        "Sie können jederzeit auf dieses Menü zugreifen, indem Sie mir den Befehl /menu senden, oder Sie können eine"
        " Beschreibung der anderen von mir unterstützten Befehle anzeigen, indem Sie mir /help senden. "
        ":smiling_face_with_smiling_eyes:",
}

MENU_COMMAND_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Here's what I can do.",
    Language.LANGUAGE_ITALIAN: "Ecco cosa posso fare.",
    Language.LANGUAGE_FRENCH: "Voici ce que je peux faire.",
    Language.LANGUAGE_GERMAN: "Folgendes kann ich tun.",
}

PRYV_ACCESS_ASKING_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH:
        "To securely store your data, we make use of Pryv. Could you grant our Bot the needed access permissions?",
    Language.LANGUAGE_ITALIAN:
        "Per archiviare in modo sicuro i tuoi dati, utilizziamo Pryv. "
        "Potresti concedere al nostro Bot le autorizzazioni di accesso necessarie?",
    Language.LANGUAGE_FRENCH:
        "Pour stocker vos données en toute sécurité, nous utilisons Pryv. "
        "Pourriez-vous accorder à notre Bot les autorisations d'accès nécessaires?",
    Language.LANGUAGE_GERMAN:
        "Um Ihre Daten sicher zu speichern, verwenden wir Pryv. "
        "Könnten Sie unserem Bot die erforderlichen Zugriffsberechtigungen erteilen?",
}

REGISTRATION_IS_MANDATORY_TO_USE_BOT_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH:
        "Granting data access consent is mandatory to use this ChatBot.",
    Language.LANGUAGE_ITALIAN:
        "La concessione del consenso per l'accesso ai dati è obbligatoria per utilizzare questo ChatBot.",
    Language.LANGUAGE_FRENCH:
        "L'autorisation d'accès aux données est obligatoire pour utiliser ce ChatBot.",
    Language.LANGUAGE_GERMAN:
        "Die Erteilung der Datenzugriffsgenehmigung ist für die Verwendung dieses ChatBot obligatorisch.",
}

PERFECT_YOU_CAN_DO_IT_WITH_FOLLOWING_LINK_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH:
        "Perfect! You can grant the permissions with the following link.\n"
        "If you don't have a Pryv account yet, you should create a new one.",
    Language.LANGUAGE_ITALIAN:
        "Perfetto! Puoi concedere le autorizzazioni con il seguente link.\n"
        "Se non hai ancora un account Pryv, dovresti crearne uno nuovo.",
    Language.LANGUAGE_FRENCH:
        "Parfait! Vous pouvez accorder les autorisations avec le lien suivant.\n"
        "Si vous n'avez pas encore de compte Pryv, vous devez en créer un nouveau.",
    Language.LANGUAGE_GERMAN:
        "Perfekt! Sie können die Berechtigungen über den folgenden Link erteilen.\n"
        "Wenn Sie noch kein Pryv-Konto haben, sollten Sie ein neues erstellen.",
}

WAITING_FOR_PRYV_REGISTRATION_MESSSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH:
        "I haven't received confirmation of your registration yet. "
        "If you have not already done so, use the link in the previous messages to grant me access to Pryv data.",
    Language.LANGUAGE_ITALIAN:
        "Non ho ricevuto la conferma della tua registrazione ancora. "
        "Se non lo hai ancora fatto usa il link nei messaggi precedenti per concedermi l'accesso ai dati di Pryv.",
    Language.LANGUAGE_FRENCH:
        "Je n'ai pas encore reçu de confirmation de votre inscription. "
        "Si vous ne l'avez pas déjà fait, utilisez le lien dans les messages précédents pour m'accorder "
        "l'accès aux données Pryv.",
    Language.LANGUAGE_GERMAN:
        "Ich habe noch keine Bestätigung Ihrer Registrierung erhalten. "
        "Wenn Sie dies noch nicht getan haben, verwenden Sie den Link in den vorherigen Nachrichten, um mir "
        "Zugriff auf Pryv-Daten zu gewähren.",
}

PRYV_ACCESS_CONFIRMED_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Pryv access granted.",
    Language.LANGUAGE_ITALIAN: "Accesso a Pryv concesso.",
    Language.LANGUAGE_FRENCH: "Accès Pryv accordé.",
    Language.LANGUAGE_GERMAN: "Pryv-Zugriff gewährt.",
}

LANGUAGE_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "What's your main language?",
    Language.LANGUAGE_ITALIAN: "Qual'è la tua lingua principale?",
    Language.LANGUAGE_FRENCH: "Quelle est votre langue principale?",
    Language.LANGUAGE_GERMAN: "Was ist deine Hauptsprache?",
}

NAME_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "What's your name?",
    Language.LANGUAGE_ITALIAN: "Qual'è il tuo nome?",
    Language.LANGUAGE_FRENCH: "Quel est ton nom?",
    Language.LANGUAGE_GERMAN: "Wie heißen Sie?",
}

AGE_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "How old are you?",
    Language.LANGUAGE_ITALIAN: "Quanti anni hai?",
    Language.LANGUAGE_FRENCH: "Quel âge avez-vous?",
    Language.LANGUAGE_GERMAN: "Wie alt bist du?",
}

SEX_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "What's your sex?",
    Language.LANGUAGE_ITALIAN: "Qual'è il tuo sesso?",
    Language.LANGUAGE_FRENCH: "Quel est ton sexe?",
    Language.LANGUAGE_GERMAN: "Was ist dein Geschlecht?",
}

FAVOURITE_SPORT_DAYS_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Which are your favourite days for doing sport in order?",
    Language.LANGUAGE_ITALIAN: "Quali sono, in ordine, i tuoi giorni preferiti in cui fare sport?",
    Language.LANGUAGE_FRENCH: "Quels sont vos jours préférés pour faire du sport dans l'ordre?",
    Language.LANGUAGE_GERMAN: "Welches sind deine Lieblingstage, um Sport zu treiben?",
}

SUPPLEMENTARY_FAVOURITE_SPORT_DAYS_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Would you like to add other favourite days?",
    Language.LANGUAGE_ITALIAN: "Vuoi aggiungere altri giorni preferiti?",
    Language.LANGUAGE_FRENCH: "Souhaitez-vous ajouter d'autres jours préférés?",
    Language.LANGUAGE_GERMAN: "Möchten Sie weitere Lieblingstage hinzufügen?",
}

DAY_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "day",
    Language.LANGUAGE_ITALIAN: "giorno",
    Language.LANGUAGE_FRENCH: "journée",
    Language.LANGUAGE_GERMAN: "Tag",
}

DAYS_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "days",
    Language.LANGUAGE_ITALIAN: "giorni",
    Language.LANGUAGE_FRENCH: "journées",
    Language.LANGUAGE_GERMAN: "Tage",
}

SPORT_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "sport",
    Language.LANGUAGE_ITALIAN: "sport",
    Language.LANGUAGE_FRENCH: "sport",
    Language.LANGUAGE_GERMAN: "Sport",
}

SPORTS_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "sports",
    Language.LANGUAGE_ITALIAN: "sport",
    Language.LANGUAGE_FRENCH: "sports",
    Language.LANGUAGE_GERMAN: "Sportarten",
}


def still_missing_text_not_localized(
        whats_missing_singular: Mapping[Language, str],
        whats_missing_plural: Mapping[Language, str],
        missing_count: int
) -> Mapping[Language, str]:
    whats_missing = whats_missing_plural if missing_count > 1 else whats_missing_singular
    return {
        Language.LANGUAGE_ENGLISH:
            f"Still {missing_count} {whats_missing[Language.LANGUAGE_ENGLISH]} to choose.",
        Language.LANGUAGE_ITALIAN:
            f"Ancora {missing_count} {whats_missing[Language.LANGUAGE_ITALIAN]} da scegliere.",
        Language.LANGUAGE_FRENCH:
            f"Encore {missing_count} {whats_missing[Language.LANGUAGE_FRENCH]} pour choisir.",
        Language.LANGUAGE_GERMAN:
            f"Noch {missing_count} {whats_missing[Language.LANGUAGE_GERMAN]} zur Auswahl.",
    }


GOALS_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Which are your goals?",
    Language.LANGUAGE_ITALIAN: "Quali sono i tuoi obiettivi?",
    Language.LANGUAGE_FRENCH: "Quels sont tes objectifs?",
    Language.LANGUAGE_GERMAN: "Welches sind deine Ziele?",
}

SELECT_OPTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Select",
    Language.LANGUAGE_ITALIAN: "Seleziona",
    Language.LANGUAGE_FRENCH: "Sélectionner",
    Language.LANGUAGE_GERMAN: "Wählen",
}

DESELECT_OPTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: ":heavy_check_mark: Selected",
    Language.LANGUAGE_ITALIAN: ":heavy_check_mark: Selezionato",
    Language.LANGUAGE_FRENCH: ":heavy_check_mark: Choisi",
    Language.LANGUAGE_GERMAN: ":heavy_check_mark: Ausgewählt",
}


def select_at_least_goals_text_not_localized(needed_count: int) -> Mapping[Language, str]:
    at_least_text = {
        Language.LANGUAGE_ENGLISH: "at least",
        Language.LANGUAGE_ITALIAN: "almeno",
        Language.LANGUAGE_FRENCH: "au moins",
        Language.LANGUAGE_GERMAN: "mindestens",
    }
    before_proceeding_text = {
        Language.LANGUAGE_ENGLISH: "before proceeding",
        Language.LANGUAGE_ITALIAN: "prima di proseguire",
        Language.LANGUAGE_FRENCH: "avant de continuer",
        Language.LANGUAGE_GERMAN: "vor dem Fortfahren",
    }
    return {
        language:
            f"{select_text} " + markup_text(f"{at_least_text[language]} {needed_count}", bold=True) +
            f" {before_proceeding_text[language]}."
        for language, select_text in SELECT_OPTION_TEXT_NOT_LOCALIZED.items()
    }


IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "I'm done :white_heavy_check_mark:",
    Language.LANGUAGE_ITALIAN: "Ho finito :white_heavy_check_mark:",
    Language.LANGUAGE_FRENCH: "J'ai fini :white_heavy_check_mark:",
    Language.LANGUAGE_GERMAN: "Ich bin fertig :white_heavy_check_mark:",
}

LETS_EVALUATE_YOUR_ABILITY_MESSAGE_TEXT = {
    Language.LANGUAGE_ENGLISH:
        "Let's evaluate your abilities now :smiling_face_with_sunglasses:\n\n"
        "You will be asked to express the degree of difficulty you feel doing some activities.\n"
        "The further you go, the more difficult the activities will be.",
    Language.LANGUAGE_ITALIAN:
        "Valutiamo le tue abilità ora :smiling_face_with_sunglasses:\n\n"
        "Ti verrà chiesto di esprimere il grado di difficoltà che provi facendo alcune attività.\n"
        "Più andrai avanti più le attivià saranno difficili.",
    Language.LANGUAGE_FRENCH:
        "Évaluons maintenant vos capacités :smiling_face_with_sunglasses:\n\n"
        "On vous demandera d'exprimer le degré de difficulté que vous ressentez à faire certaines activités.\n"
        "Plus vous irez loin, plus les activités seront difficiles.",
    Language.LANGUAGE_GERMAN:
        "Lassen Sie uns jetzt Ihre Fähigkeiten bewerten :smiling_face_with_sunglasses:\n\n"
        "Sie werden gebeten, den Schwierigkeitsgrad anzugeben, den Sie bei einigen Aktivitäten empfinden.\n"
        "Je weiter Sie gehen, desto schwieriger werden die Aktivitäten.",
}

REDO_EVALUATION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Re-evaluate ability",
    Language.LANGUAGE_ITALIAN: "Rivalutare le abilità",
    Language.LANGUAGE_FRENCH: "Réévaluer les capacités",
    Language.LANGUAGE_GERMAN: "Fähigkeiten neu bewerten",
}

REGISTRATION_COMPLETED_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Hooray! You've completed the registration :party_popper:",
    Language.LANGUAGE_ITALIAN: "Evviva! Hai completato la registrazione :party_popper:",
    Language.LANGUAGE_FRENCH: "Hourra! Vous avez terminé l'enregistrement :party_popper:",
    Language.LANGUAGE_GERMAN: "Hurra! Sie haben die Registrierung abgeschlossen :party_popper:",
}

WHICH_DATA_TO_UPDATE_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Which data would you like to update?",
    Language.LANGUAGE_ITALIAN: "Quali dati vuoi aggiornare?",
    Language.LANGUAGE_FRENCH: "Quelles données souhaitez-vous mettre à jour?",
    Language.LANGUAGE_GERMAN: "Welche Daten möchten Sie aktualisieren?",
}

NAME_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Name",
    Language.LANGUAGE_ITALIAN: "Nome",
    Language.LANGUAGE_FRENCH: "Prénom",
    Language.LANGUAGE_GERMAN: "Vorname",
}

LANGUAGE_TEXT_NOT_LOCALIZED = defaultdict(lambda: "Language")  # Not localized to make easy the language changing

SEX_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Sex",
    Language.LANGUAGE_ITALIAN: "Sesso",
    Language.LANGUAGE_FRENCH: "Sexe",
    Language.LANGUAGE_GERMAN: "Sex",
}

AGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Age",
    Language.LANGUAGE_ITALIAN: "Età",
    Language.LANGUAGE_FRENCH: "Âge",
    Language.LANGUAGE_GERMAN: "Alter",
}

FAVOURITE_SPORT_DAYS_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Favourite days for sports",
    Language.LANGUAGE_ITALIAN: "Giorni preferiti per lo sport",
    Language.LANGUAGE_FRENCH: "Journées préférées pour le sport",
    Language.LANGUAGE_GERMAN: "Lieblingstage für den Sport",
}

MODIFY_FAVOURITE_SPORT_DAYS_OPTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Days for sports",
    Language.LANGUAGE_ITALIAN: "Giorni per lo sport",
    Language.LANGUAGE_FRENCH: "Journées sportives",
    Language.LANGUAGE_GERMAN: "Tage für den Sport",
}

GOALS_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Goals",
    Language.LANGUAGE_ITALIAN: "Obiettivi",
    Language.LANGUAGE_FRENCH: "Buts",
    Language.LANGUAGE_GERMAN: "Tore",
}

LEVEL_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Current level",
    Language.LANGUAGE_ITALIAN: "Livello corrente",
    Language.LANGUAGE_FRENCH: "Niveau actuel",
    Language.LANGUAGE_GERMAN: "Aktuelles Level",
}

BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED = defaultdict(lambda: ":BACK_arrow:")

I_PROPOSE_THIS_EXERCISES_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "I propose this set of exercises ...",
    Language.LANGUAGE_ITALIAN: "Propongo questi esercizi ...",
    Language.LANGUAGE_FRENCH: "Je propose cet ensemble d'exercices ...",
    Language.LANGUAGE_GERMAN: "Ich schlage diese Übungen vor ...",
}

START_NOW_BUTTON_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: ":rocket: Start now",
    Language.LANGUAGE_ITALIAN: ":rocket: Inizia adesso",
    Language.LANGUAGE_FRENCH: ":rocket: Commencez maintenant",
    Language.LANGUAGE_GERMAN: ":rocket: Jetzt anfangen",
}

HERE_IT_IS_THE_EXERCISE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Here it is the exercise!",
    Language.LANGUAGE_ITALIAN: "Ecco l'esercizio!",
    Language.LANGUAGE_FRENCH: "Voilà l'exercice!",
    Language.LANGUAGE_GERMAN: "Hier ist es die Übung!",
}

HERE_IT_IS_THE_NEXT_EXERCISE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Here it is the next exercise!",
    Language.LANGUAGE_ITALIAN: "Ecco il prossimo esercizio!",
    Language.LANGUAGE_FRENCH: "Voici le prochain exercice!",
    Language.LANGUAGE_GERMAN: "Hier ist es die nächste Übung!",
}

TELL_ME_WHEN_FINISHED_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Tell me when you finish :smirking_face:",
    Language.LANGUAGE_ITALIAN: "Dimmi quando finisci :smirking_face:",
    Language.LANGUAGE_FRENCH: "Dis moi quand tu auras fini :smirking_face:",
    Language.LANGUAGE_GERMAN: "Sag mir, wenn Du fertig bist :smirking_face:",
}

HEY_YOU_SHOULD_EXERCISE = {
    Language.LANGUAGE_ENGLISH: "Hey! You should exercise :smirking_face:",
    Language.LANGUAGE_ITALIAN: "Hey! Dovresti fare esercizio :smirking_face:",
    Language.LANGUAGE_FRENCH: "Hey! Vous devriez exercer :smirking_face:",
    Language.LANGUAGE_GERMAN: "Hallo! Du solltest Sport treiben :smirking_face:",
}


def bot_cool_down_message_text_not_localized(cool_down_seconds: int) -> Mapping[Language, str]:
    return {
        Language.LANGUAGE_ENGLISH:
            f"My image sending functionality must cool down for {cool_down_seconds} seconds "
            f":hot_face: I'll send you only the exercise description.",
        Language.LANGUAGE_ITALIAN:
            f"La mia funzionalità di invio delle immagini deve raffreddarsi per {cool_down_seconds} secondi "
            f":hot_face: Ti invierò solo la descrizione dell'esercizio.",
        Language.LANGUAGE_FRENCH:
            f"Ma fonctionnalité d'envoi d'image doit refroidir pendant {cool_down_seconds} secondes "
            f":hot_face: Je ne vous enverrai que la description de l'exercice.",
        Language.LANGUAGE_GERMAN:
            f"Meine Bildsendefunktion muss für {cool_down_seconds} Sekunden abkühlen "
            f":hot_face: Ich schicke Ihnen nur die Übungsbeschreibung.",
    }


ABORT_SPORT_SESSION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Abort session :stop_sign:",
    Language.LANGUAGE_ITALIAN: "Interrompi sessione :stop_sign:",
    Language.LANGUAGE_FRENCH: "Abandonner la session :stop_sign:",
    Language.LANGUAGE_GERMAN: "Sitzung abbrechen :stop_sign:",
}

ARE_YOU_SURE_TO_ABORT_SESSION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Are you sure you want to abort current sport session?",
    Language.LANGUAGE_ITALIAN: "Sei sicuro di voler interrompere la sessione sportiva in corso?",
    Language.LANGUAGE_FRENCH: "Voulez-vous vraiment annuler la session sportive en cours?",
    Language.LANGUAGE_GERMAN: "Sind Sie sicher, dass Sie die aktuelle Sportsitzung abbrechen möchten?",
}

YES_BUTTON_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Yes :exclamation_mark:",
    Language.LANGUAGE_ITALIAN: "Sì :exclamation_mark:",
    Language.LANGUAGE_FRENCH: "Oui :exclamation_mark:",
    Language.LANGUAGE_GERMAN: "Ja :exclamation_mark:",
}

NO_BUTTON_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "No ...",
    Language.LANGUAGE_ITALIAN: "No ...",
    Language.LANGUAGE_FRENCH: "Non ...",
    Language.LANGUAGE_GERMAN: "Nein ...",
}

HOW_MUCH_DIFFICULT_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "How difficult was this exercise?",
    Language.LANGUAGE_ITALIAN: "Quanto era difficile questo esercizio?",
    Language.LANGUAGE_FRENCH: "À quel point cet exercice a-t-il été difficile?",
    Language.LANGUAGE_GERMAN: "Wie schwierig war diese Übung?",
}

TOO_DIFFICULT_TRY_WITH_EASIER_EXERCISES_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH:
        "Ok, this was too much for you. Don't worry! Next time I'll propose you easier exercises :winking_face:",
    Language.LANGUAGE_ITALIAN:
        "Ok, questo era troppo per te. Non preoccuparti! "
        "La prossima volta ti proporrò esercizi più facili :winking_face:",
    Language.LANGUAGE_FRENCH:
        "Ok, c'était trop pour toi. Ne t'inquiète pas! "
        "La prochaine fois je vous proposerai des exercices plus faciles :winking_face:",
    Language.LANGUAGE_GERMAN:
        "Ok, das war zu viel für dich. Mach dir keine Sorgen! "
        "Nächstes Mal werde ich Ihnen einfachere Übungen vorschlagen :winking_face:",
}

DID_YOU_HAVE_FUN_QUESTION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "What was it like doing these exercises?",
    Language.LANGUAGE_ITALIAN: "Come è stato fare questi esercizi?",
    Language.LANGUAGE_FRENCH: "Comment était-ce de faire ces exercices?",
    Language.LANGUAGE_GERMAN: "Wie war es, diese Übungen zu machen?",
}

GOOD_JOB_HERES_THE_SESSION_SUMMARY_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Well done! Here's your sport session summary:",
    Language.LANGUAGE_ITALIAN: "Molto bene! Ecco il riepilogo della sessione sportiva:",
    Language.LANGUAGE_FRENCH: "Bien joué! Voici le résumé de votre session sportive:",
    Language.LANGUAGE_GERMAN: "Gut gemacht! Hier ist Ihre Zusammenfassung der Sportsitzungen:",
}

YOUR_RATING_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Perceived difficulty",
    Language.LANGUAGE_ITALIAN: "Difficoltà percepita",
    Language.LANGUAGE_FRENCH: "Difficulté perçue",
    Language.LANGUAGE_GERMAN: "Wahrgenommene Schwierigkeit",
}

DURATION_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Duration",
    Language.LANGUAGE_ITALIAN: "Durata",
    Language.LANGUAGE_FRENCH: "Durée",
    Language.LANGUAGE_GERMAN: "Dauer",
}

NEW_LEVEL_REACHED_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Difficulty level updated!",
    Language.LANGUAGE_ITALIAN: "Livello di difficoltà aggiornato!",
    Language.LANGUAGE_FRENCH: "Niveau de difficulté mis à jour!",
    Language.LANGUAGE_GERMAN: "Schwierigkeitsgrad aktualisiert!",
}

HERE_ARE_YOUR_STATISTICS_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Here are your statistics :chart_increasing:",
    Language.LANGUAGE_ITALIAN: "Ecco le tue statistiche :chart_increasing:",
    Language.LANGUAGE_FRENCH: "Voici vos statistiques :chart_increasing:",
    Language.LANGUAGE_GERMAN: "Hier sind Ihre Statistiken :chart_increasing:",
}

CHOOSE_DIFFERENT_EXERCISE_SETS_WITH_ARROWS_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "You can choose a different exercise set using the arrows.",
    Language.LANGUAGE_ITALIAN: "Puoi scegliere un diverso set di esercizi usando le frecce.",
    Language.LANGUAGE_FRENCH: "Vous pouvez choisir un ensemble d'exercices différent à l'aide des flèches.",
    Language.LANGUAGE_GERMAN: "Mit den Pfeilen können Sie einen anderen Übungssatz auswählen.",
}

WHERE_WE_SAVE_YOUR_DATA_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Where we save your data",
    Language.LANGUAGE_ITALIAN: "Dove salviamo i tuoi dati",
    Language.LANGUAGE_FRENCH: "Où nous sauvegardons vos données",
    Language.LANGUAGE_GERMAN: "Wo wir Ihre Daten speichern",
}

YOUR_DATA_IS_STORED_IN_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Your data is stored in: ",
    Language.LANGUAGE_ITALIAN: "I tuoi dati sono archiviati in: ",
    Language.LANGUAGE_FRENCH: "Vos données sont stockées en: ",
    Language.LANGUAGE_GERMAN: "Ihre Daten werden gespeichert in: ",
}

FOR_WHICH_PURPOSE_WE_SAVE_YOUR_DATA_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "For which purpose we keep your data",
    Language.LANGUAGE_ITALIAN: "Per quale scopo conserviamo i tuoi dati",
    Language.LANGUAGE_FRENCH: "Dans quel but nous conservons vos données",
    Language.LANGUAGE_GERMAN: "Zu diesem Zweck speichern wir Ihre Daten",
}

WHO_CAN_ACCESS_YOUR_DATA_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Who can access your data",
    Language.LANGUAGE_ITALIAN: "Chi può acedere ai tuoi dati",
    Language.LANGUAGE_FRENCH: "Qui peut accéder à vos données",
    Language.LANGUAGE_GERMAN: "Wer kann auf Ihre Daten zugreifen",
}

WHICH_AGENT_BEHAVIOUR_USE_YOUR_DATA_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Which agents behaviours use your data",
    Language.LANGUAGE_ITALIAN: "Quali comportamenti degli agenti utilizzano i tuoi dati",
    Language.LANGUAGE_FRENCH: "Quels comportements des agents utilisent vos données",
    Language.LANGUAGE_GERMAN: "Welche Agentenverhalten verwenden Ihre Daten",
}
