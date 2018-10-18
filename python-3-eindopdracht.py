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

def kies_lijst(lijst_naam):
    '''wijzigt de variabele die de bestandsnaam van de geselecteerde lijst onthoud.'''
    global nuLijstNaam
    nuLijstNaam = lijst_naam

def leeg_scherm():
    '''leegt het scherm.'''
    os.system('cls' if os.name == 'nt' else 'clear')

def woordenlijst_tekst(woordenlijst):
    '''returneert de woordenlijst als een leesbare string met uitlijning en enters'''
    woordenlijstTekst = ""
    for woord in woordenlijst:
        if woord[0] != ".":
            woordenlijstTekst += "{:>30} = {}\n".format(woord, woordenlijst[woord])
    return(woordenlijstTekst)

def lees_woordenlijst(bestandsnaam):
    '''leest het bestand, geeft errors mee in de dictionary'''
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

def schrijf_woordenlijst(bestandsnaam, woordenlijst):
    '''schrijft de gegeven dictionary naar de gegeven bestandslocatie/naam, overschrijft als nodig.'''
    bestand = open(bestandsnaam, "w")

    for woord in woordenlijst:
        bestand.write("{}={}\n".format(woord, woordenlijst[woord]))

    bestand.close()

def main():
    '''Dit is het main menu. Vanaf hier kan je naar alle functies navigeren'''
    while True: # herhaal totdat de afsluiten() functie is aangeroepen. Dit doet een sys.exit.
        print_menu(nuLijstNaam) # print alle kiesbare commando's met betekenissen
        answer = input("Antwoord hier: ")
        if answer == NIEUWE_LIJST:
            nieuwe_lijst() # maakt een nieuwe lijst, laat je woorden toevoegen en sslaat de lijst op.
        elif answer == KIES_LIJST:
            kies_nieuwe_lijst() # laat je een nieuwe lijst selecteren en controleert of die lijst bestaat en leesbaar is.
        elif answer == TOEVOEGEN:
            voeg_woorden_toe(nuLijstNaam) # laat je woorden toevoegen/verwijderen aan de lijst op de gegeven bestandslocatie.
        elif answer == ALLE:
            voeg_woordenlijst_toe(nuLijstNaam) # laat je een gehele lijst importeren.
        elif answer == OVERHOREN:
            overhoren(nuLijstNaam) # Leest en overhoort de woordenlijst op de gegeven bestandslocatie.
        elif answer == STOPPEN:
            afsluiten() # print een afscheid en sluit alles af.
        else:
            print_popup("Het commando '{}' is geen kiesbaar commando.".format(answer))

def nieuwe_lijst():
    '''maakt een nieuwe lijst, laat je woorden toevoegen en sslaat de lijst op.'''
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

def overhoren(woordenlijstnaam):
    '''Leest en overhoort de woordenlijst op de gegeven bestandslocatie.'''
    woorden = lees_woordenlijst(woordenlijstnaam)
    if woorden[".error"] != "succesvol":
        print_popup("Kon woordenlijst {} niet overhoren.\n{}".format(woordenlijstnaam, woorden[".error"]))
        return
    del woorden[".error"]

    print_popup("Woordenlijst {} wordt overhoort.".format(woordenlijstnaam))
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

def print_afscheid():
    '''print een afscheid.'''
    print('\n' * SCHERMHOOGTE)
    print('tot ziens!')
    print('         |"" |\  /|  /| ')
    print('MADE BY: |   | \/ | /_|_')
    print('         |__ |    |   | ')
    print('codemaker4.github.io')

def print_header():
    '''print de bovenkant van een window.'''
    print(LIJNH * SCHERMBREEDTE)
    print(LIJNV + ' '*(SCHERMBREEDTE-2) + LIJNV)

def print_regel(inhoud=''):
    '''print de gegeven tekst tussen zij streepjes in. combineer met print_header() en print_footer() voor het printen van een volledig window met tekst.'''
    string = "{}  {:" + str(SCHERMBREEDTE-6) + "}  {}"
    print(string.format(LIJNV, inhoud, LIJNV))

def print_footer():
    '''print de bovenkant van een onderkant.'''
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
    '''leegt het scherm en print alle componenten van een window met de gegeven tekst erin.'''
    leeg_scherm()
    print_header()
    tekstRegels = tekst.split("\n")
    for tekstRegel in tekstRegels:
        print_regel(tekstRegel)
    print_footer()

def print_menu(lijst_naam):
    '''print de tekst voor het main menu'''
    print_window("Hier is het centrale keuzemenu:\n\nJe hebt nu lijst {} geselecteerd.\n{} = nieuwe woordenlijst maken\n{} = veranderen van woordenlijst.\n{} = toevoegen/verwijderen van woorden in woordenlijst {}.\n{} = woordenlijst importeren.\n{} = woordenlijst {} overhoren\n{} = programma afsluiten".format(lijst_naam, NIEUWE_LIJST, KIES_LIJST, TOEVOEGEN, lijst_naam, ALLE, OVERHOREN, lijst_naam, STOPPEN))

def print_popup(tekst):
    '''print een wondow met de gegeven tekst + 'druk op enter om door te gaan' erin en wacht totdat de gebruiker op enter drukt.'''
    print_window("{}\n\ndruk op enter om door te gaan".format(tekst))
    input() # gegeven iput wordt niet onthouden/gebruikt. Het wacht alleen totdat de gebruiker iets invoert (dus op enter drukt)

def kies_nieuwe_lijst():
    '''laat je een nieuwe lijst selecteren en controleert of die lijst bestaat en leesbaar is.'''
    print_window("Kies de naam van de lijst.\nTyp '{}' om te annuleren.".format(STOPPEN))
    answer = input("Typ hier: ")
    if answer == STOPPEN:
        return
    bestandsnaam = answer + EXTENSIE
    if lees_woordenlijst(bestandsnaam)[".error"][-11:] == "niet vinden":
        print_popup("'{}' bestaat niet.".format(bestandsnaam))
    elif lees_woordenlijst(bestandsnaam)[".error"][-14:] == "niet begrijpen":
        print_popup("'{}' is geen geldige woordenlijst.".format(bestandsnaam))
    else:
        kies_lijst(bestandsnaam)
        print_popup("'{}' is gekozen.".format(bestandsnaam))

def verwijder_woord(woordenlijst, woordenlijstNaam):
    '''laat je een woord uit de specifieke lijst verwijderen. Krijgt de dictionary IPV een bestadslocatie en retourneert de dictionary zonder het eventueel verwijderde woord IPV de dictionary zelf opteslaan.'''
    aanHetZoeken = True
    while aanHetZoeken:
        print_window("Typ het woord dat je wilt verwijderen.\nHier is de lijst:\n{}\ntyp {} om te annuleren".format(woordenlijst_tekst(woordenlijst), STOPPEN))
        antwoord = input("Typ hier: ")
        if antwoord == STOPPEN:
            aanHetZoeken = False
        else:
            print_window("zoeken...")
            for woord in woordenlijst:
                if antwoord == woord:
                    woord = antwoord
                    del woordenlijst[woord]
                    aanHetZoeken = False
                    break
        if aanHetZoeken:
            print_popup("Het antwoord {} is geen commando of woord. Probeer het opnieuw.\nTIP: het werkt alleen met het woord VOOR de '='.".format(antwoord))
        return woordenlijst

def voeg_woorden_toe(lijst_naam):
    '''laat je woorden toevoegen/verwijderen aan de lijst op de gegeven bestandslocatie.'''
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

def voeg_woordenlijst_toe(lijst_naam):
    '''laat je een gehele lijst importeren'''
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
    '''print een afscheid en sluit alles af'''
    print_afscheid()
    sys.exit()

main()
