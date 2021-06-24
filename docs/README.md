# Garah Train Timetable

Het **Garah Train Timetable**-formaat (kortweg ook **GATT**) is een formaat voor het beschrijven van de dienstregeing van treinen, primair ontworpen voor het maken van een reisplanner voor het geofictieprojet [Garah](https://garah.nl/).

Het formaat biedt ondersteuning voor de definitie van vervoerders, stations en andere dienstregelingspunten, treintypes, treinseries en treinen, en maakt gebruik van het [TOML-formaat](https://toml.io/), dat makkelijk leesbaar is voor zowel mensen als computers.

Zie [example.toml](example.toml) voor een voorbeeldbestand, gebaseerd op [NS-treinserie 500](https://wiki.ovinnederland.nl/wiki/Treinserie_500_(2021)) van Rotterdam Centraal naar Groningen.

## Specificatie

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

### Feed-informatie

Feed-informatie wordt bovenin het bestand gedefinieerd (zonder tabelnaam tussen vierkante haken) en bevat de volgende velden:

Naam | Type | Verplicht| Beschrijving
--- | --- | --- | ---
`feed_name` | `string` | Nee | De naam van het GATT-bestand.
`feed_author` | `string` | Nee | De auteur van het GATT-bestand.
`feed_description` | `string` | Nee | Een optionele beschrijving van het GATT-bestand.
`script` | `string` | Nee | Indien gedefinieerd geeft dit veld weer welke transliteratie gebruikt moet worden voor het weergeven van namen.


#### Voorbeelden

Een voorbeeld van feed-informatie:

```toml
feed_name = "Tunaran"
feed_author = "Danae"
feed_description = "Dienstregeling ggebaseerd op het basisuurpatroon van Tunaran"
script = "ludivi_merigami"
````

### Vervoerders

Vervoerders worden gedefinieerd in de `agencies`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht| Beschrijving
--- | --- | --- | ---
`name` | `string` | **Ja** | De naam van de vervoerder.
`abbr` | `string` | Nee | De afkorting van de vervoerder.
`description` | `string` | Nee | Een optionele beschrijving van de vervoerder.

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

### Stations en dienstregelingspunten

Stations en dienstregelingspunten worden gedefinieerd in de `nodes`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht |  Beschrijving
--- | --- | --- | ---
`name` | `string` | **Ja** | De naam van het station.
`short_name` | `string` | Nee | De korte naam van het station.
`abbr` | `string` | Nee | De afkorting van het station.
`description` | `string` | Nee | Een optionele beschrijving van het station.
`x` of `lon` | `float` | Nee | De x-coördinaat of de lengtegraad van het station.
`y` of `lat` | `float` | Nee | De y-coördinaat of de breedtegraad van het station.
`type` | `string` | Nee | Het type van het station of dienstregelingspunt, waarbij een van de later genoemde waarden gebruikt kan worden. Indien weggelaten wordt dit veld ingesteld op `station`.
`node` | `boolean` | Nee | Geeft aan of dit station een knooppuntstation is (`true`) of niet (`false`). Indien weggelaten wordt dit veld ingesteld op `false`.
`train_types` | `array` | Nee | Leeg | Een lijst van ids van treintypes die op dit station stoppen. Indien weggelaten wordt dit veld ingesteld op een lege lijst.
`on_call` | `boolean` | Nee | `false` | Geeft aan of dit station alleen op afroep wordt bediend (`true`) of dat alle treinen hier stoppen (`false`). Indien weggelaten wordt dit veld ingesteld op `false`.

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

### Treintypes

Treintypes worden gedefinieerd in de `train_types`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht | Beschrijving
--- | --- | --- | ---
`name` | `string` | **Ja** | De naam van het treintype.
`abbr` | `string` | Nee | De afkorting van het treintype.
`description` | `string` | Nee | Een optionelebeschrijving van het treintype.
`priority` | `string` | Nee | De prioriteit van het treintype, waarbij snellere treintypes doorgaans een lager prioriteitsnummer hebben. Indien weggelaten wordt dit veld ingesteld op 0.

#### Voorbeelden

Een voorbeeld van een `train_types`-tabel:

```toml
[train_types]
nl_ic = {name = "Intercity", abbr = "IC"}
nl_spr = {name = "Sprinter", abbr = "SPR"}
```

Een voorbeeld van een `train_types`-tabel met subtabellen:

```toml
[train_types.nl_ic]
name = "Intercity"
abbr = "IC"

[train_types.nl_spr]
name = "Sprinter"
abbr = "IC"
```

### Treinseries

Treinseries worden gedefinieerd in de `train_sets`-tabel en bevatten de volgende velden:

Naam | Type | Verplicht | Beschrijving
--- | --- | --- | ---
`agency` | `string` | **Ja** | De id van de vervoerder van de treinserie.
`type` | `string` | **Ja** | De id van het treintype van de treinserie.
`name` | `string` | **Ja** | De naam van de treinserie.
`abbr` | `string` | Nee | De afkorting van de treinserie.
`description` | `string` | Nee | Een optionele beschrijving van de treinserie.
`priority` | `int` | Nee | De prioriteit van de trein. Indien weggelaten wordt de prioriteit van het treintype gebruikt.
`color_text` | `string` | Nee | De kleur van de tekst wanneer de treinserie als lijnnummer wordt weergegeven. Indien weggelaten wordt de standaard kleur gebruikt.
`color_bg` | `string` | Nee | De kleur van de achtergrond wanneer de treinserie als lijnnummer wordt weergegeven. Indien weggelaten wordt de standaard kleur gebruikt.
`route` | `table` | Nee | De route van de treinserie.

De `route`-tabel van een treinserie bevat routepunten met de volgende velden:

Naam | Type | Verplicht | Beschrijving
--- | --- | --- | ---
`type` | `string` | **Ja** | Het type van het routepuntwaarbij een van de later genoemde waarden gebruikt kan worden.
`node` | `string` | **Ja** | De id van het station van het routepunt.
`platform` | `string` | Nee | Het spoor waarop de trein stopt.
`a` | `string` | Zie verder | De tijd waarop de trein op dit station aankomt in de vorm `HH:MM`. Verplicht bij types `stop` en `end`.
`d` | `string` | Zie verder | De tijd waarop de trein van dit station vertrekt in de vorm `HH:MM`. Verplicht bij types `begin` en `stop`.

Voor `type` kunnen de volgende waarden gebruikt worden:

Waarde | beschrijving
--- | ---
`begin` | Begin van de route. Het veld `d` moet worden gedefinieerd als vertrektijd.
`stop` | Een punt waar de treinserie stopt. De velden `d` en `a` moeten beide worden gedefinieerd als resp. vertrektijd en aankomsttijd.
`over` | Een punt dat de treinserie passeert zonder te stoppen. De velden `d` en `a` zijn beide optioneel en geven de passeertijd weer.
`end` | Eind van de route. Het veld `a` moet worden gedefinieerd als aankomsttijd.

#### Voorbeelden

Een voorbeeld van een `train_series` tabel met subtabellen (het wordt aanbevolen om voor de treintypes geen korte variant te gebruiken vanwege de complexere structuur vna een treinserie):

```toml
[train_sets.nl_500]
agency = "ns"
type = "IC"
name = "IC 500 Rotterdam Centraal - Leeuwarden"
abbr = "500"

[train_sets.nl_500.route]
00 = {type = 'begin', station = "nl_rtd", d = "00:05"}
01 = {type = 'stop', station = "nl_rtda", a = "00:12", d = "00:13"}
02 = {type = 'stop', station = "nl_gd", a = "00:23", d = "00:24"}
03 = {type = 'stop', station = "nl_ut", a = "00:42", d = "00:49"}
04 = {type = 'stop', station = "nl_amf", a = "01:02", d = "01:04"}
05 = {type = 'stop', station = "nl_zl", a = "01:39", d = "01:45"}
06 = {type = 'stop', station = "nl_asn", a = "02:24", d = "02:25"}
07 = {type = 'end', station = "nl_gn", a = "02:42"}
```

### Treinen

Treinen kunnen op twee manieren worden gedefinieerd in de `trains`-tabel:
* Wanneer een trein onderdeel is van een treinserie, bevat een trein de volgende velden:

Naam | Type | Verplicht | Beschrijving
--- | --- | --- | ---
`set` | `string` | **Ja** | De id van de treinserie van deze trein.
`time` | `string` | **Ja** | De vertrektijd van deze trein in de vorm `HH:MM`. De vertrek- een aankomsttijden van de treinserie worden bij deze waarde opgeteld; een `time` van 07:00 met als `d` van het eerste routepunt om 00:15 vertrekt dus daadwerkelijk om 07:15
`begin_at` | `string` | Nee | Indien gespecificeerd begint de trein bij het routepunt met deze id. Laat leeg om bij het begin van de route te beginnen.
`end_at` | `string` | Nee | Indien gespecificeerd eindigt de trein bij het routepunt met deze id. Laat leeg om bij het einde van de route te eindigen.
`agency` | `string` | Nee | De id van de vervoerder van de trein als deze afwijkt van de vervoerder van de treinserie.
`type` | `string` | Nee | De id van het treintype van de trein als deze afwijkt van het treintype van de treinserie.
`name` | `string` | Nee | De naam van de trein als deze afwijkt van de naam van de treinserie.
`abbr` | `string` | Nee | De afkorting van de trein als deze afwijkt van de afkorting van de treinserie.
`description` | `string` | Nee | Een optionele beschrijving van de trein.
`color_text` | `string` | Nee | De kleur van de tekst wanneer de treinserie als lijnnummer wordt weergegeven. Indien weggelaten wordt de kleur van de treinserie gebruikt.
`color_bg` | `string` | Nee | De kleur van de achtergrond wanneer de treinserie als lijnnummer wordt weergegeven. Indien weggelaten wordt de kleur van de treinserie gebruikt.
`priority` | `int` | Nee | De prioriteit van de trein. Indien weggelaten wordt de prioriteit van het treinserie gebruikt.

* Wanneer een trein een losstaande trein is, d.w.z. geen onderdeel van een treinserie, worden dezelfde velden gebruikt als bij een treinserie, zoals hierboven gespecificeerd. Belangrijk is dat een losstaande trein altijd een `route`-attribuut heeft.

#### Voorbeelden

Een voorbeeld van een `trains`-tabel:

```toml
[trains]
nl_515 = {set = "nl_500", time = "05:00", begin_at_point = "05"}
nl_519 = {set = "nl_500", time = "06:00"}
nl_523 = {set = "nl_500", time = "07:00"}
nl_527 = {set = "nl_500", time = "08:00"}
```

Een voorbeeld van een `trains`-tabel met subtabellen:
```toml
[trains.nl_515]
series = "500"
time = "05:00"
begin_at_point = "05"
```
