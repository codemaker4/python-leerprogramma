import sys
import os
import random

DELETE = 'd'
EXTENSIE = '.wrd'
KIES_LIJST = 'k'
MAX_WOORDLENGTE = 20
NIEUWE_LIJST = 'n'
OPSLAAN = 'w'
OVERHOREN = 'o'
SCHEIDER = '='
LIJNH = '='
LIJNV = '|'
SCHERMBREEDTE = 137
SCHERMHOOGTE = 64
STANDAARD_LIJST = 'test.wrd'
STOPPEN = 'q'
TOEVOEGEN = 't'
ALLE = 'a'

nuLijstNaam = STANDAARD_LIJST
# nuLijstData = ['Error, probeer de lijst opnieuw te laden']

def kies_lijst(lijst_naam):
    global nuLijstNaam
    nuLijstNaam = lijst_naam

def leeg_scherm():
    # print('\n' * SCHERMHOOGTE)
    os.system('cls' if os.name == 'nt' else 'clear')
  #        Gebruikt: SCHERMHOOGTE
  #        Parameters: -
  #        Returnwaarde: -

def woordenlijst_tekst(woordenlijst):
    woordenlijstTekst = ""
    for woord in woordenlijst:
        if woord[0] != ".":
            woordenlijstTekst += "{:>30} = {}\n".format(woord, woordenlijst[woord])
    return(woordenlijstTekst)

def lees_woordenlijst(bestandsnaam):
    GelezenWoordenlijst = {".error": "succesvol"}
    try:
        with open(bestandsnaam) as f:
            regels = f.read().split("\n")
    except:
        GelezenWoordenlijst[".error"] = "error: kon {} niet vinden".format(bestandsnaam)
        return GelezenWoordenlijst

    try:
        for regel in regels:
            woorden = regel.split(SCHEIDER)
            print(woorden)
            if len(woorden) == 2:
                GelezenWoordenlijst[woorden[0]] = woorden[1]
            elif not len(woorden) <= 1:
                GelezenWoordenlijst[".error"] = "error: kon {} niet begrijpen".format(bestandsnaam)
                print(len(woorden))
    except:
        GelezenWoordenlijst[".error"] = "error: error tijdens het begrijpen van {}".format(bestandsnaam)
    return GelezenWoordenlijst
  #     Leest de woordparen in uit het bestand genaamd 'bestandsnaam'.
  #
  #     Gebruikt: SCHEIDER
  #     Parameter: naam van het bestand waar de woordenlijst in staat
  #     Returnwaarde: een dictionary met woordparen

def schrijf_woordenlijst(bestandsnaam, woordenlijst):
    bestand = open(bestandsnaam, "w")

    for woord in woordenlijst:
        bestand.write("{}={}\n".format(woord, woordenlijst[woord]))

    bestand.close()
  #         Schrijft de woordparen weg naar het bestand genaamd 'bestandsnaam'.
  #         De oude inhoud van het bestand wordt overschreven!
  #
  #         Gebruikt: SCHEIDER
  #         Parameter: naam van het bestand waar de woordenlijst in geschreven wordt, woordenlijst die weggeschreven wordt
  #         Returnwaarde: -

def main():
    while True:
        print_menu(nuLijstNaam)
        answer = input("Antwoord hier: ")
        if answer == NIEUWE_LIJST:
            nieuwe_lijst()
        elif answer == KIES_LIJST:
            kies_nieuwe_lijst()
        elif answer == TOEVOEGEN:
            voeg_woorden_toe(nuLijstNaam)
        elif answer == ALLE:
            voeg_woordenlijst_toe(nuLijstNaam)
        elif answer == OVERHOREN:
            overhoren(nuLijstNaam)
        elif answer == STOPPEN:
            afsluiten()
        else:
            print_popup("Het commando '{}' is geen kiesbaar commando.".format(answer))
  #         Laat een keuzemenu zien
  #
  #         Op zijn minst zijn de volgende keuzes mogelijk:
  #          - nieuwe woordenlijst maken
  #          - veranderen van woordenlijst
  #          - woorden toevoegen aan een woordenlijst
  #          - woordenlijsten overhoren
  #          - stoppen met het programma
  #
  #         De gebruiker kan vervolgens steeds nieuwe keuzes blijven maken.
  #
  #         Gebruikt: STANDAARD_LIJST, KIES_LIJST, OVERHOREN, TOEVOEGEN, EXTENSIE, STOPPEN
  #         Parameters: Geen
  #         Returnwaarde: Geen

def nieuwe_lijst():
    # while True:
    print_window("Kies de naam van de nieuwe lijst. \nTyp '{}' om te annuleren.".format(STOPPEN))
    answer = input("Antwoord hier: ")
    if answer == STOPPEN:
        return
    if len(answer) < 2:
        print_popup("'{}' is een te korte naam. Kies een langere naam.".format(answer))
        return
    bestandsnaam = answer + EXTENSIE
    print_window("Lijst '{}' maken...".format(bestandsnaam))
    if lees_woordenlijst(bestandsnaam)[".error"][-11:] == "niet vinden": # als de lijst nog niet bestaat
        schrijf_woordenlijst(bestandsnaam, {}) # maak de lijst aan
    kies_lijst(bestandsnaam) # kies de lijst
    print_popup("Lijst '{}' gemaakt.\nDeze lijst is nu ook geselecteerd.\nNu kan je woorden toevoegen.".format(bestandsnaam))
    voeg_woorden_toe(bestandsnaam)
    return

  # maak een nieuw bestand aan voor een nieuwe lijst en vraagt meteen om woorden toe te voegen.

def nieuwe_lijst_naam():
    pass
        # Gebruikt: -
        # Parameters: -
        # Returnwaarde: de lijst_naam van de nieuw gekozen lijst

def overhoren(woordenlijst):
    woorden = lees_woordenlijst(woordenlijst)
    if woorden[".error"] != "succesvol":
        print_popup("Kon woordenlijst {} niet overhoren.\n{}".format(woordenlijst, woorden[".error"]))
        return
    del woorden[".error"]

    print_popup("Woordenlijst {} wordt overhoort.".format(woordenlijst))
    playing = True
    while playing:
        if random.randrange(0,2) < 1:
            question, corrAnswer = random.choice(list(woorden.items()))
        else:
            corrAnswer, question = random.choice(list(woorden.items()))
        hintLetters = ["-"] * len(corrAnswer)
        hintVolgorde = []
        for i in range(0,len(corrAnswer)):
            hintVolgorde += [i]
        random.shuffle(hintVolgorde)
        pogingen = 0
        while True:
            print_window("Wat is {}?\nHint: {}\nTyp /{} om te stoppen".format(question, "".join(hintLetters), STOPPEN))
            answer = input("antwoord hier:")
            if len(answer) == 0:
                pass
            elif answer[0] == "/":
                if answer == "/"+STOPPEN:
                    playing = False
                    break
                else:
                    print_popup("{} is geen commando.".format(answer))
            elif answer == corrAnswer:
                print_popup("Je had het goed na {} pogingen!".format(pogingen))
                break
            else:
                print_popup("{} is niet goed, probeer het nog eens.".format(answer))
            pogingen += 1
            if pogingen > len(corrAnswer):
                print_popup("Het antwoord was: {}".format(corrAnswer))
                break
            hintLetters[hintVolgorde[pogingen-1]] = corrAnswer[hintVolgorde[pogingen-1]]

  #         Blijf woorden overhoren totdat de gebruiker aangeeft te willen stoppen.
  #
  #         Gebruikt: STOPPEN
  #         Parameters: de woordenlijst die overhoord moet worden
  #         Returnwaarde: -

def print_afscheid():
        print('\n' * SCHERMHOOGTE)
        print('tot ziens!')
        print('         |"" |\  /|  /| ')
        print('MADE BY: |   | \/ | /_|_')
        print('         |__ |    |   | ')
        print('codemaker4.github.io')

        # Gebruikt: SCHERMHOOGTE, SCHERMBREEDTE
        # Parameters: -
        # Returnwaarde: -

def print_header():
    print(LIJNH * SCHERMBREEDTE)
    print(LIJNV + ' '*(SCHERMBREEDTE-2) + LIJNV)
  #         Print het volgende over de hele breedte van het scherm:
  #         ===============
  #         |             |
  #         Dus een volle regel met '='-tekens en een regel die begint en eindigt met een '|'.
  #
  #         Gebruikt: SCHERMBREEDTE
  #         Parameters: -
  #         Returnwaarde: -

def print_regel(inhoud=''):
    string = "{}  {:" + str(SCHERMBREEDTE-6) + "}  {}"
    print(string.format(LIJNV, inhoud, LIJNV))
  #         print_regel() print de inhoud links uitgelijnd uit.
  #         Voor de inhoud wordt '| ' gezet en rechts uitgelijnd ' |'.
  #         Bijvoorbeeld:
  #         SCHERMBREEDTE = 30
  #         inhoud = "Mooi zeg"
  #         Uitvoer:
  #         | Mooi zeg                   |
  #
  #         Gebruikt: SCHERMBREEDTE
  #         Parameters: de string die geprint moet worden in de regel
  #         Returnwaarde: -

def print_footer():
    print(LIJNV + ' '*(SCHERMBREEDTE-2) + LIJNV)
    print(LIJNH * SCHERMBREEDTE)
  #         Print het volgende over de hele breedte van het scherm:
  #         |             |
  #         ===============
  #         Dus een volle regel met '='-tekens en een regel die begint en eindigt met een '|'.
  #
  #         Gebruikt: SCHERMBREEDTE
  #         Parameters: -
  #         Returnwaarde: -

def print_window(tekst):
    leeg_scherm()
    print_header()
    tekstRegels = tekst.split("\n")
    for tekstRegel in tekstRegels:
        print_regel(tekstRegel)
    print_footer()

def print_menu(lijst_naam):
            print_window("Hier is het centrale keuzemenu:\n\nJe hebt nu lijst {} geselecteerd.\n{} = nieuwe woordenlijst maken\n{} = veranderen van woordenlijst.\n{} = toevoegen/verwijderen van woorden in woordenlijst {}.\n{} = woordenlijst importeren.\n{} = woordenlijst {} overhoren\n{} = programma afsluiten".format(lijst_naam, NIEUWE_LIJST, KIES_LIJST, TOEVOEGEN, lijst_naam, ALLE, OVERHOREN, lijst_naam, STOPPEN))
  #         Print het (keuze)menu inclusief de geselecteerde lijst
  #
  #         Gebruikt: SCHERMHOOGTE, SCHERMBREEDTE
  #         Parameters: De naam van de geselecteerde woordenlijst
  #         Returnwaarde: -

def print_popup(tekst):
    print_window("{}\n\ndruk op enter om door te gaan".format(tekst))
    input()

def kies_nieuwe_lijst():
    while True:
        print_window("Kies de naam van de lijst.\nTyp '{}' om te annuleren.".format(STOPPEN))
        answer = input("Typ hier: ")
        bestandsnaam = answer + EXTENSIE
        print(lees_woordenlijst(bestandsnaam)[".error"][-14:])
        if answer == STOPPEN:
            return
        elif lees_woordenlijst(bestandsnaam)[".error"][-11:] == "niet vinden":
            print_popup("'{}' bestaat niet.".format(bestandsnaam))
        elif lees_woordenlijst(bestandsnaam)[".error"][-14:] == "niet begrijpen":
            print_popup("'{}' is geen geldige woordenlijst.".format(bestandsnaam))
        else:
            kies_lijst(bestandsnaam)
            break

def verwijder_woord(woordenlijst, woordenlijstNaam):
    aanHetZoeken = True
    while aanHetZoeken:
        print_window("Typ het woord dat je wilt verwijderen.\nHier is de lijst:\n{}\ntyp {} om te annuleren".format(woordenlijst_tekst(woordenlijst), STOPPEN))
        antwoord = input("Typ hier: ")
        if antwoord == STOPPEN:
            return woordenlijst
        else:
            print_window("zoeken...")
            for woord in woordenlijst:
                if antwoord == woord:
                    aanHetZoeken = False
        if aanHetZoeken:
            print_popup("Het antwoord {} is geen commando of woord. Probeer het opnieuw.\nTIP: het werkt alleen met het woord VOOR de '='.".format(antwoord))
    woord = antwoord
    del woordenlijst[woord]
    return woordenlijst
  #         Vraagt of gebruiker zeker weet of er verwijderd moet worden.
  #         Verwijdert het woord en de vertaling uit de lijst als dit zo is.
  #
  #         Gebruikt: -
  #         Parameters: het woord dat verwijderd moet worden, de woordenlijst waaruit verwijderd moet worden
  #         Returnwaarde: -

def voeg_woorden_toe(lijst_naam):
    woorden = lees_woordenlijst(lijst_naam)
    if woorden[".error"] != "succesvol":
        print_popup("Kon wordenlijst {} niet lezen:\n{}".format(lijst_naam, woorden[".error"]))
        return
    del woorden[".error"]
    antwoord = ""
    while True:
        print_window("Woordenlijst: {}\nWoorden:\n{}\nTyp '[woord] = [woord]' om woorden aan de lijst toe te voegen.\nTyp '{}' om een woord te verwijderen.\nTyp '{}' om te stoppen en deze lijst op te slaan.".format(lijst_naam, woordenlijst_tekst(woorden), DELETE, STOPPEN))
        antwoord = input("Typ hier: ")
        splitAntwoord = antwoord.split(" = ")
        if antwoord == STOPPEN:
            schrijf_woordenlijst(lijst_naam, woorden)
            return
        elif antwoord == DELETE:
            woorden = verwijder_woord(woorden, lijst_naam)
        elif len(splitAntwoord) == 2:
            woorden[splitAntwoord[0]] = splitAntwoord[1]
            print(woorden)
        else:
            print_popup("'{}' is geen commando of toevoegbaar woord.".format(antwoord))

  #         Vraag de gebruiker steeds om woordenparen en voeg ze toe aan de lijst.
  #         Stop als de gebruiker aangeeft te willen stoppen.
  #
  #         Gebruikt: SCHEIDER, STOPPEN
  #         Parameters: de woordenlijst waarin toegevoegd moet worden, de lijst_naam van deze woordenlijst
  #         Returnwaarde: -

def voeg_woordenlijst_toe(lijst_naam):
        woorden = lees_woordenlijst(lijst_naam)
        if woorden[".error"] != "succesvol":
            print_popup("Kon wordenlijst {} niet lezen:\n{}".format(lijst_naam, woorden[".error"]))
            return
        del woorden[".error"]
        print_window("Dit is de interface waarmee je grote lijsten met woorden kan toevoegen.\nvoer hier de schijder in.\nAlles dat je meegeeft wordt van de woorden afgehaald.\nVaak is dit alleen maar een tab.\nAls je het echt niet weet kan je kladblok of een ander simpel tekstprogramma openen en daar het symbool uit kopieren.")
        tempScheider = input("Voer hier het symbool in: ")
        errors = []
        print_window("Alles staat klaar. Nu hoef je alleen maar de tekst in te voeren.\nDit doe je door de woorden te selecteren, CTRL+C in te drukken,\nTerug naar dit programma te gaan en CTRL+V te drukken (voor windows)\ntyp '\klaar' als de woorden zijn ingevoerd.")
        answer = ""
        while True:
            answer = input("Plak de woorden hier, typ '/klaar als dit klaar is.': ")
            if answer == "/klaar":
                break
            try:
                splitAnswer = answer.split(tempScheider)
                if len(splitAnswer) == 2:
                    if len(splitAnswer[0]) > 0 and len(splitAnswer[1]) > 0:
                        woorden[splitAnswer[0]] = splitAnswer[1]
                    else:
                        errors += ["Error: '{}': een van de woorden '{}', '{}' is 0 karakters lang.".format(answer, splitAnswer[0], splitAnswer[1])]
                else:
                    errors += ["Error: '{}': er zijn {} woorden gevonden, terwijl alleen exact 2 woorden zijn toegestaan.".format(answer, len(splitAnswer))]
            except:
                errors += ["Error: '{}': iets ging helemaal mis.".format(answer)]

        while True:
            print_window("Het toevoegen van woorden is klaar.\nEr zijn {} errors gevonden.\ntyp 'e' om de errors te bekijken.\ntyp '{}' om op te slaan\ntyp '{}' om te annuleren.".format(len(errors), OPSLAAN, STOPPEN))
            answer = input("typ hier: ")
            if answer == STOPPEN:
                return
            elif answer == OPSLAAN:
                schrijf_woordenlijst(lijst_naam, woorden);
                return
            elif answer == "e":
                errorString = ""
                for error in errors:
                    errorString += error + "\n"
                print_popup("Hier zijn de errors:\n{}".format(errorString))
            else:
                print_popup("{} is geen commando.".format(answer))

def afsluiten():
    print_afscheid()
    sys.exit()

# voeg_woorden_toe("test.txt")
#
# print_popup('dat ging niet goed')
# print_afscheid()
# print_header()
# print_regel('dit is een test')
# print_footer()

main()

afsluiten()
