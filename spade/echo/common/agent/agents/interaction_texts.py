from collections import defaultdict

from common.chat.language_enum import Language

NEW_USER_MESSAGE_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "It seems you're a new user!",
    Language.LANGUAGE_ITALIAN: "Sembra che tua sia un nuovo utente!",
    Language.LANGUAGE_FRENCH: "Il semble que vous soyez un nouvel utilisateur!",
    Language.LANGUAGE_GERMAN: "Sie scheinen ein neuer Benutzer zu sein!",
}

BOT_INTRODUCTION_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH:
        "I am EchoBot, the robot that can help you doing physical activity! :flexed_biceps:",
    Language.LANGUAGE_ITALIAN:
        "Sono EchoBot, il robot che può aiutarti a fare attività fisica! :flexed_biceps:",
    Language.LANGUAGE_FRENCH:
        "Je suis EchoBot, le robot qui peut vous aider à faire de l'activité physique! :flexed_biceps:",
    Language.LANGUAGE_GERMAN:
        "Ich bin EchoBot, der Roboter, der Ihnen bei körperlicher Aktivität helfen kann! :flexed_biceps:",
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

ECHO_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "You're now in the Echo state. I will repeat everything you write to me!",
    Language.LANGUAGE_ITALIAN: "Ora sei nello stato Echo. Ripeterò tutto quello che mi scrivi!",
    Language.LANGUAGE_FRENCH: "Tu es maintenant dans l'état d'Écho. Je répéterai tout ce que tu m'écrirez!",
    Language.LANGUAGE_GERMAN: "Du befinden dich jetzt im Echo-Zustand. "
                              "Ich werde alles wiederholen was du mir schreiben!",
}

IM_DONE_RESPONSE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "I'm done :check_mark_button:",
    Language.LANGUAGE_ITALIAN: "Ho finito :check_mark_button:",
    Language.LANGUAGE_FRENCH: "J'ai fini :check_mark_button:",
    Language.LANGUAGE_GERMAN: "Ich bin fertig :check_mark_button:",
}

REGISTRATION_COMPLETED_MESSAGE_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "Hooray! You've completed the registration :party_popper:",
    Language.LANGUAGE_ITALIAN: "Evviva! Hai completato la registrazione :party_popper:",
    Language.LANGUAGE_FRENCH: "Hourra! Vous avez terminé l'enregistrement :party_popper:",
    Language.LANGUAGE_GERMAN: "Hurra! Sie haben die Registrierung abgeschlossen :party_popper:",
}

NAME_TEXT_NOT_LOCALIZED = {
    Language.LANGUAGE_ENGLISH: "First Name",
    Language.LANGUAGE_ITALIAN: "Nome",
    Language.LANGUAGE_FRENCH: "Prénom",
    Language.LANGUAGE_GERMAN: "Vorname",
}

LANGUAGE_TEXT_NOT_LOCALIZED = defaultdict(lambda: "Language")  # Not localized to make easy the language changing

BACK_TO_PREVIOUS_MENU_BUTTON_TEXT_NOT_LOCALIZED = defaultdict(lambda: ":BACK_arrow:")

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
