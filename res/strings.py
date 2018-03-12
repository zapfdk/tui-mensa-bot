__author__ = "zapfdk"

STRINGS = {
    "start": "Willkommen beim TU Ilmenau Mensabot",

    "help": "/start Starte den Bot\n\
\n\
/help Bekomme Hilfe für die Nutzung des Mensa Bots\n\
\n\
/sub [mensakürzel] Abonniere den Speiseplan für die angegeben Mensen, z.B. so:\n\
*/sub ehren nano*\n\
um den Speiseplan für die Mensa Ehrenberg und die Nanoteria zu erhalten.\n\
Mögliche Kürzel: ehren, nano, roentgen\n\
Um den Speiseplan für alle Mensen zu erhalten, könnt ihr die Kürzel einfach weglassen und nur /sub eingeben.\n\
\n\
/unsub Deabonniere den Speiseplan\n\
\n\
/time HH:MM - Stelle die Uhrzeit für deinen Speiseplan ein. Ersetze dafür HH:MM für die Uhrzeit zu der du den Speiseplan bekommen willst\n\
\n\
/menu Bekomme einmalig den Speiseplan zugeschickt. Hier gelten die gleichen Kürzel wie beim /sub Befehl.\n\
\n\
/rate Bewerte dein heutiges Essen auf einer Skala von 1 bis 5\n\
\n\
/stats Erhalte aktuelle Statistiken über den Bot\n\
\n\
/feedback Kontaktiere den Admin für Feedback, Bugs, Infos oder ein paar nette Worte :)\n\
\n\
Disclaimer:\n\
Keine Gewähr auf die Korrektheit des Speiseplans.\n\
Für die Funktionsfähigkeit des Bots wird lediglich deine Chat ID ohne weitere Kontaktangaben gespeichert.\n\
Die durch die Bewertungsfunktion gesammelten Daten werden daher auch nicht personenbezogen sondern nur zur Erhebung von Statistiken verwendet.\n\
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
