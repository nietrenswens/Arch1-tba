"""Verzameling van alle beschrijvingen"""

locdesc_dict = {
    "start": "Dit lijkt de top van de berg te zijn. Richting het oosten lijkt er een pad te zijn. Richting het noorden zie je een klif. Het zuiden en westen zijn dichtgegroeid met bomen.",
    "klif": "Het pad lijkt hier abrupt te stoppen, een klif. Je kijkt naar beneden. Het is te hoog om de grond te zien. Richting het zuiden zie je een plek wat de top van de berg lijkt te zijn",
    "bostop": "Je loopt een bos in. Het is donker maar iets verderop hoor je een vreemd gehuil....\nJe loopt verder... Het gehuil wordt steeds luider.\nAchter een gigantische steen ligt een gestrande walvis. \
Walvis: '..... h .. eeel p..... \n...\n..  please ...... make it stop....' Richting het westen zie je een pad dat omhoog loopt. Richting het zuiden zie je een pad het bos in leidt. Richting het oosten zie je de bomen minderen en lijk je een huisje te zien.",
    "klifhuis": "Iets verderop zie je een kleine chalet staan. 'Dit zou het echt goed doen op AirBnB', denk je bij jezelf. Je opent de deur...\n\
Er staan geen meubels in de chalet. Richting het westen kan je terug lopen.",
    "bostopzuid": "Je loopt verder naar beneden door het bos. Je wordt omringd door de groene natuur en voelt de rust zich over je lichaam wassen...\
\nIneens voel je iets scherps om je been klemmen... 'AUAAAA' schreeuw je uit. Wanneer je naar beneden kijkt zie je dat je volop in een berenval bent gestapt.\
\n...Gelukkig heb je dit een keer op Discovery Channel gezien... Je drukt met beide handen de veren aan de zijkant van de berenval omlaag.\
\nDe berenval opent en je haalt voorzichtig je been er uit... Je bloedt echter flink. Je voelt je lichtjes in je hoofd. Richting het zuiden zie je een pad dat dieper het bos in leidt. Richting het noorden zie je een pad wat naar een minderbegroeid deel van het bos lijkt te gaan.",
    "dehethek": "Verder het bos in staat voor je ineens een enorm hek. Aan de opening hangt een slot. Je kan alleen terug richting het noorden, tenzij het hek open kan.",
    "appiebos": "Dieper in het bos is het nogal donker. Het lijkt hier dood te lopen. Je kan alleen richting het westen terug.",
    "klifsprong": "Iets verderop kom je weer bij een klif uit... Het lijkt erop dat dit de enige weg van de berg af is. Richting het oosten zie je de poort.",
    "henk": "Pas wanneer je met beide benen op de grond staat kijk je op en zie je een heel bekend gezicht... HENK...\
\nIneens herinner je je alles. 'Jij was het.... door jou zit ik hier al dagen vast... Jij hebt mij uit het vliegtuig geduwd.\
\n'Ik kan het uitle-', Henk kan zijn zin niet afmaken. Je rent op hem af klaar om te vechten.",
    "rekenmachinebos": "Overal waar je heen gaat lijkt alleen maar naar meer bos te leiden. Ook dit lijkt weer op een dood einde.",
    "tovenaar": "Je loopt verder naar beneden... Het lijkt erop dat je met dit pad eindelijk de berg afkomt.\
\nJe stopt abrupt met lopen, maar dit gaat tegen je wil in. Het voelt plots alsof er blokken ijzer aan je beide benen hangen.\
\nJe kijkt omhoog en ziet een schimmig silhouette staan. Het silhouette komt dichterbij en langzamerhand zie je het gezicht van de man.\
\nHij heeft een lange punthoed op en een overduidelijk neppe baard op zijn gezicht gelijmd...\
\n'Ik ben de almachtige tovenaar van de berg en niemand verlaat deze berg zonder mijn raadsel op te lossen' schreeuwt hij. \nDit zou best intimiderend zijn als hij geen nepbaard op had.\
\n'Om langs mij te komen moet je een eeuwenoud raadsel oplossen, maar enkele zielen hebben dit raadsel kunnen beantwoorden. Ik geef je 1 kans. \nHet raadsel luidt als volgt...\
\n..........    2  +  2  =  ?",
}

itemdesc_dict = {
    "parachute" : "Een parachute. Hij ziet er hevig beschadigd uit. Zal hij nog werken?" + "|" + \
        "Een parachute. Hij ziet er hevig beschadigd uit. Zal hij nog werken?",
    "zuurstoftank" : "Een zuurstoftank met ongeveer 50% capaciteit. De tank is duidelijk al over de datum, maar ziet er nog steeds goed uit, en is nog steeds bruikbaar." + "|" \
        + "Een zuurstoftank met ongeveer 50% capaciteit. De tank is duidelijk al over de datum, maar ziet er nog steeds goed uit, en is nog steeds bruikbaar.",
    "vis": "Een grote vis. De vis laat je hongerig voelen, maar hij flopt al de klif af voordat je hem kan pakken." + "|" + "Een grote vis. De vis laat je hongerig voelen, maar hij flopt al de klif af voordat je hem kan pakken.",
    "steen": "Een glimmende steen. Hij doet je denken aan je kindertijd." + "|" + "Een glimmende steen. Hij doet je denken aan je kindertijd.",
    "tak": "Een grote scherpe tak naast de walvis..." + "|" + "Een tak. Hij is erg zwaar.",
    "spons": "uit een boomstronk een spons steken." + "|" + "Een natte spons. Hij is erg zwaar en nat. Waarom heb je hem opgepakt?",
    "sleutel": "In de borstkas van de walvis glimt iets... Het lijkt op een sleutel." + "|" + "Een sleutel. Er zit nog wat bloed op.",
    "jonko": "Naast het raampje zie je een dikke jonko liggen naast een verroestte Zippo aansteker." + "|" + "Een jonko. Hij is niet insi gedraaid...",
    "bacardi": "Uit de grond steekt een fles met een rode dop. Het is een fles Bacardi Lemon." + "|" + "Bacardi Lemon. Het label is vervaagd.",
    "mobiel": "In het gras zie je iets oplichten en hoor je een bekend getril. Een mobiel." + "|" + "Een mobiel. Het scherm is gebarsten.",
    "tas": "aan de tak van een boom iets blauws. Het is een Albert Heijn tasje." + "|" + "Een AH tasje. Hij is nog in perfecte staat.",
    "rekenmachine": "Naast een boom zie je een muis met een GR zitten." + "|" + "Een grafische rekenmachine. Hij werkt nog. Het schermpje is moeilijk leesbaar."
}

def getItemDesc(itemname: str):
    return itemdesc_dict[itemname].split("|")[0]

def getHeldDesc(itemname: str):
    return itemdesc_dict[itemname].split("|")[1]
