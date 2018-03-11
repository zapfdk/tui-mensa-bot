__author__ = "zapfdk"

STRINGS = {
    "start": "Willkommen beim TU Ilmenau Mensabot",

    "help": "/start Starte den Bot\
        \
        /help Bekomme Hilfe für die Nutzung des Mensa Bots\
        \
        /sub [mensakürzel] Abonniere den Speiseplan für die angegeben Mensen, z.B. so:\
        /sub ehren nano\
        um den Speiseplan für die Mensa Ehrenberg und die Nanoteria zu erhalten.\
        Mögliche Kürzel: ehren, nano, roentgen\
        Um den Speiseplan für alle Mensen zu erhalten, könnt ihr die Kürzel einfach weglassen und nur /sub eingeben.\
        \
        /unsub Deabonniere den Speiseplan\
        \
        /time HH:MM - Stelle die Uhrzeit für deinen Speiseplan ein. Ersetze dafür HH:MM für die Uhrzeit zu der du den Speiseplan bekommen willst\
        \
        /menu Bekomme einmalig den Speiseplan zugeschickt. Hier gelten die gleichen Kürzel wie beim /sub Befehl.\
        \
        /rate Bewerte dein heutiges Essen auf einer Skala von 1 bis 5\
        \
        /stats Erhalte aktuelle Statistiken über den Bot\
        \
        /feedback Kontaktiere den Admin für Feedback, Bugs, Infos oder ein paar nette Worte :)\
        \
        Disclaimer:\
        Keine Gewähr auf die Korrektheit des Speiseplans.\
        Für die Funktionsfähigkeit des Bots wird lediglich deine Chat ID ohne weitere Kontaktangaben gespeichert.\
        Die durch die Bewertungsfunktion gesammelten Daten werden daher auch nicht personenbezogen sondern nur zur Erhebung von Statistiken verwendet.\
        Der TUIMensaBot ist ein studentisches Freizeitprojekt und steht weder mit der TU Ilmenau noch dem StW Thüringen in Verbindung.",

    "rate": {
        "already_rated": "Tut mir leid, aber du kannst nur ein Essen am Tag bewerten.",
        "choose_food": "Wähle das Essen aus, das du heute bewerten willst:",
        "choose_rating": "Wieviele Sterne würdest du deinem Essen geben?",
        "thanks": "Danke für's Bewerten!"
    },

    "feedback": {
        "thanks": "Danke für dein Feedback!",
        "no_feedback": "Du solltest schon etwas dazu schreiben ;)",
    },

    "sub": {
        "success": "Du hast den Speiseplan für {subbed_mensas} abonniert.",
        "invalid_short_name": "Eins deiner eingegebenen Mensakürzel war ungülstig, bitte wähle eines oder mehrere aus dieser Liste: "
    },

    "unsub": {
        "success": "Du hast den Speiseplan deabonniert."
    },

    "time": {
        "wrong_arg": "Gib bitte eine Uhrzeit im Format HH:MM ein.",
        "success": "Du hast deine Uhrzeit auf {sub_time} gestellt."
    },

    "stats": "Aktuelle Statistiken:\n" \
               "{total_users} bisher gesehene Benutzer\n" \
               "{subbed_users} aktuelle Nutzer\n" \
               "{ratings} abgegebene Bewertungen\n",
}
