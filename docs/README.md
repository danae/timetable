# Garah Train Timetable

Het **Garah Train Timetable**-formaat (kortweg ook **GATT**) is een formaat voor het beschrijven van de dienstregeing van treinen, primair ontworpen voor het maken van een reisplanner voor het geofictieprojet [Garah](https://garah.nl/).

Het formaat biedt ondersteuning voor de definitie van vervoerders, stations en andere dienstregelingspunten, treintypes, treinseries en treinen, en maakt gebruik van het [TOML-formaat](https://toml.io/), dat makkelijk leesbaar is voor zowel mensen als computers.

Zie [example.toml](example.toml) voor een voorbeeldbestand, gebaseerd op [NS-treinserie 500](https://wiki.ovinnederland.nl/wiki/Treinserie_500_(2021)) van Rotterdam Centraal naar Groningen.

## 1. Specificatie

Een GATT-bestand werkt net als een database en bestaat uit verschillende tabellen. Een tabel wordt op de volgende manier gedefinieerd:

* De header bestaat uit de tabelnaam tussen vierkante haken `[]`;
* Hierna volgt op elke regel een element uit de tabel. De id van het element staat voor het =-teken, de velden van het element daarna tussen gekrulde haken `{}`.

```toml
[agencies]
nl_ns = {name = "Nederlandse Spoorwegen", abbr = "NS"}
nl_db = {name = "Deutsche Bahn", abbr = "DB"}
```

Het is ook mogelijk om elk element uit de tabel als eigen tabel te definieren. Beide stijlen kunnen door elkaar gebruikt worden:
* De header bestaat uit de tabelnaam, gevolgd door een punt en de id van het element tussen vierkante haken `[]`;
* Elk veld van het element volgt daarna op een aparte regel.

```toml
[agencies.nl_ns]
name = "Nederlandse Spoorwegen"
abbr = "NS"

[agencies.nl_db]
name = "Deutsche Bahn"
abbr = "DB"
```

Indien een id andere tekens bevat dan alfanumerieke tekens of een underscore `A-Z 0-9 _`, moet deze tussen aanhalingstekens ``""`` worden geschreven; `nl_500` en `[agencies.nl_500a]` kunnen dus zonder aanhalingstekens worden geschreven, maar `[agencies."at_öbb"]` moet met aanhalingstekens worden geschreven. Het woordt aanbevolen om alleen alfanumerieke tekens en underscores in ids te gebruiken.

### 1.1. Feed-informatie

Feed-informatie wordt bovenin het bestand gedefinieerd (zonder tabelnaam tussen vierkante haken) en bevat de volgende velden:

Naam | Type | Verplicht| Beschrijving
--- | --- | --- | ---
`feed_id` | `string` | Nee | De id van de feed.
`feed_name` | `string` | Nee | De naam van de feed.
`feed_author` | `string` | Nee | De auteur de feed.
`script` | `string` | Nee | Indien gedefinieerd geeft dit veld weer welke transliteratie gebruikt moet worden voor het weergeven van namen.


#### Voorbeelden

Een voorbeeld van feed-informatie:

```toml
feed_id = "tun"
feed_name = "Dienstregeling van Tunaran"
feed_author = "Danae"
script = "ludivi_merigami"
````

### 1.2. Vervoerders

Vervoerders worden gedefinieerd in de `agencies`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht| Beschrijving
--- | --- | --- | ---
`name` | `string` | **Ja** | De naam van de vervoerder.
`abbr` | `string` | Nee | De afkorting van de vervoerder.

#### Voorbeelden

Een voorbeeld van een `agencies`-tabel:

```toml
[agencies]
nl_ns = {name = "Nederlandse Spoorwegen", abbr = "NS"}
nl_db = {name = "Deutsche Bahn", abbr = "DB"}
```

Een voorbeeld van een `agencies`-tabel met subtabellen:

```toml
[agencies.nl_ns]
name = "Nederlandse Spoorwegen"
abbr = "NS"

[agencies.nl_db]
name = "Deutsche Bahn"
abbr = "DB"
```

### 1.3. Stations en dienstregelingspunten

Stations en dienstregelingspunten worden gedefinieerd in de `nodes`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht |  Beschrijving
--- | --- | --- | ---
`name` | `string` | **Ja** | De naam van het station.
`short_name` | `string` | Nee | De korte naam van het station.
`abbr` | `string` | Nee | De afkorting van het station.
`type` | `string` | Nee | Het type van het station of dienstregelingspunt, waarbij een van de later genoemde waarden gebruikt kan worden. Indien weggelaten wordt dit veld ingesteld op `station`.
`x` of `lon` | `float` | Nee | De x-coördinaat of de lengtegraad van het station.
`y` of `lat` | `float` | Nee | De y-coördinaat of de breedtegraad van het station.
`node` | `boolean` | Nee | Geeft aan of dit station een knooppuntstation is (`true`) of niet (`false`). Indien weggelaten wordt dit veld ingesteld op `false`.
`modalities` | `array` | Nee | Een lijst van ids van vervoerswijzen die op dit station stoppen. Indien weggelaten wordt dit veld ingesteld op een lege lijst.
`remarks` | `table` | Nee | Opmerkingen behorend tot het station in de vorm van een tabel zoals hieronder beschreven.
`services` | `table` | Nee | Voorzieningen behorend tot het station in de vorm van een tabel zoals hieronder beschreven.

Voor `type` kunnen de volgende waarden gebruikt worden:

Waarde | Beschrijving
--- | ---
`unspecified` |  Niet nader gespecificeerd
`station` | Station
`split` | Splitsing
`over` | Inhaalspoor op de vrije baan
`cross` | Overloopwissel (kruisingsmogelijkheid op de vrije baan)
`fork` | Aansluiting (splitsingspunt op de vrije baan)
`bridge` | Beweegbare spoorbrug
`border` | Grenspost

De `remarks`-tabel van een station kan de volgende optionele velden bevatten:

Naam | Type | Beschrijving
--- | --- | ---
`on_call` | `boolean` | Geeft aan of dit station alleen op afroep wordt bediend (`true`) of dat alle treinen hier stoppen (`false`).

De `services`-tabel van een station kan de volgende optionele velden bevatten:

Naam | Type | Beschrijving
--- | --- | ---
*Nog geen velden gedefinieerd.* | |

#### Voorbeelden

Een voorbeeld van een `nodes`-tabel:

```toml
[nodes]
nl_rtd = {name = "Rotterdam Centraal", node = true, train_types = ["nl_ic", "nl_spr"]}
nl_rtda = {name = "Rotterdam Alexander", train_types = ["nl_ic", "nl_spr"]}
nl_gd = {name = "Gouda", node = true, train_types = ["nl_ic", "nl_spr"]}
nl_ut = {name = "Utrecht Centraal", node = true, train_types = ["nl_ic", "nl_spr"]}
```

Een voorbeeld van een `nodes`-tabel met subtabellen:

```toml
[nodes.nl_rtd]
name = "Rotterdam Centraal"
short_name = "Rotterdam C"
type = "station"
node = true
train_types = ["nl_ic", "nl_spr"]

[nodes.nl_rtda]
name = "Rotterdam Alexander"
short_name = "Alexander"
type = "station"
train_types = ["nl_ic", "nl_spr"]
```

### 1.4. Vervoerswijzen

Een vervoerswijze is de manier waarop passagiers vervoerd worden, zoals een trein, tram, metro of bus. Vervoerswijzen worden gedefinieerd in de `modalities`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht | Beschrijving
--- | --- | --- | ---
`name` | `string` | **Ja** | De naam van de vervoerswijze.
`abbr` | `string` | Nee | De afkorting van de vervoerswijze.
`description` | `string` | Nee | Een optionelebeschrijving van de vervoerswijze.
`type` | `string` | Nee | Het type van de vervoerswijze, waarbij een van de later genoemde waarden gebruikt kan worden. Indien weggelaten wordt dit veld ingesteld op `rail`.
`priority` | `string` | Nee | De prioriteit van het treintype, waarbij snellere treintypes doorgaans een lager prioriteitsnummer hebben. Indien weggelaten wordt dit veld ingesteld op 0.
`color_text` | `string` | Nee | De kleur van de tekst wanneer de vervoerswijze als lijnnummer wordt weergegeven. Indien weggelaten wordt de standaard kleur gebruikt.
`color_bg` | `string` | Nee | De kleur van de achtergrond wanneer de vervoerswijze als lijnnummer wordt weergegeven. Indien weggelaten wordt de standaard kleur gebruikt.

Voor `type` kunnen de volgende waarden gebruikt worden:

Waarde | Beschrijving
--- | ---
`tram` |  Tram of lightrail; elk lightrailsysteem of railsysteem op straatniveau in een stedelijk gebied
`subway` | Metro; elk ondergronds srailysteem in een stedelijk gebied
`rail` | Trein; railvervoer tussen steden of op lange afstand
`bus` | Bus; busvervoer op korte en lange afstand
`ferry` | Veerboot; bootvervoer op korte en lange afstand
`cable_car` | Kabeltram; railsystemen op straatniveau die door een kabel wordt voortgetrokken
`aerial_lift` | Kabelbaan; aan een kabel hangende cabines of gondels die door die kabel worden voortgetrokken
`funicular` | Funiculaire; railsysteem ontworpen om grote hoogteverschillen te overbruggen
`trolleybus` | Trolleybus; elektrich busvervoer waarbij stroom via bovenleidingen wordt afgenomen
`monorail` | Monorail; railsysteem waarbij de baan bestaat uit een enkele rail

#### Voorbeelden

Een voorbeeld van een `modalities`-tabel:

```toml
[modalities]
nl_ic = {name = "Intercity", abbr = "IC", type = "rail", priority = 1}
nl_spr = {name = "Sprinter", abbr = "SPR", type = "rail", priority = 2}
```

Een voorbeeld van een `modalities`-tabel met subtabellen:

```toml
[modalities.nl_ic]
name = "Intercity"
abbr = "IC"
type = "rail"
priority = 1

[modalities.nl_spr]
name = "Sprinter"
abbr = "IC"
type = "rail"
priority = 2
```

### 1.5. Routes

Een route is een verzameling van trips die dezelfde stations en dienstregelingspunten passeren. Een voorbeeld van een route is een treinserie. Routes worden gedefinieerd in de `routes`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht | Beschrijving
--- | --- | --- | ---
`agency` | `string` | **Ja** | De id van de vervoerder van de route.
`modality` | `string` | **Ja** | De id van de vervoerswijze van de route.
`stops` | `table` | **Ja** | De punten waar de route stopt of die de route passeert.
`name` | `string` | **Ja** | De naam van de route.
`abbr` | `string` | Nee | De afkorting van de route.
`priority` | `int` | Nee | De prioriteit van de route. Dit veld kan worden ingevuld als deze afwijkt van de prioriteit van de vervoerswijze.
`remarks` | `table` | Nee | Opmerkingen behorend tot de route in de vorm van een tabel zoals hieronder beschreven.
`services` | `table` | Nee | Voorzieningen behorend tot de route in de vorm van een tabel zoals hieronder beschreven.
`color_text` | `string` | Nee | De kleur van de tekst wanneer de route als lijnnummer wordt weergegeven. Dit veld kan worden ingevuld als deze afwijkt van de tekstkleur van de vervoerswijze.
`color_bg` | `string` | Nee | De kleur van de achtergrond wanneer de route als lijnnummer wordt weergegeven. Dit veld kan worden ingevuld als deze afwijkt van de achtergrondkleur van de vervoerswijze.

Een route kan een `stops`-tabel definiëren voor een abstract overzicht van de routepunten waar deze route stopt of die deze route passeert.
* Indien er een `stops`-tabel in de route wordt gedefinieerd, moet in elke trip die is gekoppeld aan deze route een veld `time` worden gedefinieerd.
* Indien er **geen** `stops`-tabel in de route wordt gedefinieerd, moet elke trip die is gekoppeld aan deze route een eigen `stops`-tabel definiëren volgens de hieronder beschreven specificatie.

De `remarks`-tabel van een route kan de volgende optionele velden bevatten:

Naam | Type | Beschrijving
--- | --- | ---
`international` | `boolean` | Deze trein overschrijdt een landsgrens. Zorg voor geldige reisdocumenten!
`res_recommended` | `boolean` | Voor deze trein is een reservering aanbevolen.
`res_required` | `boolean` | Voor deze trein is een reservering verplicht.
`supplement` | `boolean` | Voor deze trein dient een toeslag te worden betaald.

De `services`-tabel van een route kan de volgende optionele velden bevatten:

Naam | Type | Beschrijving
--- | --- | ---
`night_service` | `boolean` | Nachttrein
`sleeping_car` | `boolean` | Slaaprijtuig
`first_only` | `boolean` | Alleen eerste klas
`second_only` | `boolean` | Alleen tweede klas
`coffee` | `boolean` | Koffieautomaat
`bistro` | `boolean` | Bistro aan boord
`restaurant` | `boolean` | Restauratierijtuig
`luggage` | `boolean` | Bagageafdeling

#### Voorbeelden

Een voorbeeld van een `route` tabel met subtabellen (het wordt aanbevolen om voor de routes geen korte variant te gebruiken vanwege de complexere structuur van een route):

```toml
[route.nl_500]
agency = "ns"
modality = "IC"
name = "IC 500 Rotterdam Centraal - Leeuwarden"
abbr = "500"

[route.nl_500.stops]
00 = {node = "nl_rtd", d = "00:05"}
01 = {node = "nl_rtda", a = "00:12", d = "00:13"}
02 = {node = "nl_gd", a = "00:23", d = "00:24"}
03 = {node = "nl_ut", a = "00:42", d = "00:49"}
04 = {node = "nl_amf", a = "01:02", d = "01:04"}
05 = {node = "nl_zl", a = "01:39", d = "01:45"}
06 = {node = "nl_asn", a = "02:24", d = "02:25"}
07 = {node = "nl_gn", a = "02:42"}
```

### 1.6. Trips

Een trip is een specifieke rit van een route die op een bepaalde tijd wordt gereden. Trips worden gedefinieerd in de `trips`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht | Beschrijving
--- | --- | --- | ---
`route` | `string` | **Ja** | De id van de route van deze trip.
`stops` | `table` | **Ja** | De punten waar de trip stopt of die de trip passeert. Zie verder voor een uitleg wanneer dit veld gedefinieerd moet worden.
`time` | `string` | **Ja** | De vertrektijd van deze trip in de vorm `HH:MM`. Zie verder voor een uitleg wanneer dit veld gedefinieerd moet worden.
`begin_at` | `string` | Nee | Indien gespecificeerd begint de trip bij het station met deze id. Laat leeg om bij het begin van de route te beginnen.
`end_at` | `string` | Nee | Indien gespecificeerd eindigt de trip bij het station met deze id. Laat leeg om bij het einde van de route te eindigen.
`agency` | `string` | Nee | De id van de vervoerder van de trip. Dit veld kan worden ingevuld als deze afwijkt van de vervoerder van de route.
`modality` | `string` | Nee | De id van de vervoerswijze van de trip. Dit veld kan worden ingevuld als deze afwijkt van de vervoerswijze van de route.
`name` | `string` | Nee | De naam van de trip. Dit veld kan worden ingevuld als deze afwijkt van de naam van de route.
`abbr` | `string` | Nee | De afkorting van de trein. Dit veld kan worden ingevuld als deze afwijkt van de afkorting van de route.
`priority` | `int` | Nee | De prioriteit van de trip. Dit veld kan worden ingevuld als deze afwijkt van de prioriteit van de route.
`remarks` | `table` | Nee | Opmerkingen behorend tot de trip in de vorm van een tabel zoals beschreven onder routes. Dit veld kan worden ingevuld als deze afwijkt van de opmerkingen van de route.
`services` | `table` | Nee | Voorzieningen behorend tot de trip in de vorm van een tabel zoals beschreven onder routes. Dit veld kan worden ingevuld als deze afwijkt van de voorzieningen van de route.
`color_text` | `string` | Nee | De kleur van de tekst wanneer de trip als lijnnummer wordt weergegeven. Dit veld kan worden ingevuld als deze afwijkt van de tekstkleur van de route.
`color_bg` | `string` | Nee | De kleur van de achtergrond wanneer de trip als lijnnummer wordt weergegeven. Dit veld kan worden ingevuld als deze afwijkt van de achtergrondkleur van de route.

Een trip moet ofwel een veld `time` of een `stops`-tabel definiëren.
* Indien de gekoppelde route een `stops`-tabel heeft gedefinieerd, moet de trip een veld `time` definieren met de relatieve vertrektijd die wordt opgeteld bij de tijden in de `stops`-tabel van de route. Wanneer bijvoorbeeld een veld `time` van 07:30 wordt gedefinieerd en de `stops`-tabel van de route de tijden 00:15, 00:18 en 00:20 heeft gedefinieerd, worden deze voor de trip ingesteld op resp. 7:45, 7:48 en 7:50.
* Indien de gekoppelde route **geen** `stops`-tabel heeft gedefinieerd, moet de trip een eigen `stops`-tabel definiëren volgens de hieronder beschreven specificatie.

#### Voorbeelden

Een voorbeeld van een `trips`-tabel:

```toml
[trips]
nl_515 = {route = "nl_500", time = "05:00", begin_at_point = "05"}
nl_519 = {route = "nl_500", time = "06:00"}
nl_523 = {route = "nl_500", time = "07:00"}
nl_527 = {route = "nl_500", time = "08:00"}
```

Een voorbeeld van een `trips`-tabel met subtabellen:
```toml
[trips.nl_515]
route = "500"
time = "05:00"
begin_at = "05"
```

### 1.7. Stops

De `stops`-tabel van een route of trip bevat een lijst van routepunten met de volgende velden:

Naam | Type | Verplicht | Beschrijving
--- | --- | --- | ---
`node` | `string` | **Ja** | De id van het station dat bij dit routepunt hoort.
`platform` | `string` | Nee | Het perron waar het vervoermiddel stopt.
`a` | `string` | **Ja** | De tijd waarop het vervoermiddel bij dit routepunt aankomt in de vorm `HH:MM`. Moet worden weggelaten bij het eerste routepunt.
`d` | `string` | **Ja** | De tijd waarop het vervoermiddel van dit routepunt vertrekt in de vorm `HH:MM`. Moet worden weggelaten bij het laatste routepunt.
`skip` | `boolean` | Nee | Geeft aan of het vervoermiddel bij dit routepunt stopt (`false`) of het alleen passeert (`true`). indien weggelaten wordt dit veld ingesteld op `false`.

#### Voorbeelden

Een voorbeeld van een `stops`-tabel van een route:

```toml
[route.nl_500.stops]
00 = {node = "nl_rtd", d = "00:05"}
01 = {node = "nl_rtda", a = "00:12", d = "00:13"}
02 = {node = "nl_gd", a = "00:23", d = "00:24"}
03 = {node = "nl_ut", a = "00:42", d = "00:49"}
04 = {node = "nl_amf", a = "01:02", d = "01:04"}
05 = {node = "nl_zl", a = "01:39", d = "01:45"}
06 = {node = "nl_asn", a = "02:24", d = "02:25"}
07 = {node = "nl_gn", a = "02:42"}
```
