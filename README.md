## Bestandsformaat

Een feed bestaat uit een of meerdere bestanden in het [TOML-formaat](https://toml.io/). Deze bestanden hebben de extensie `.toml` of `.gatt`, met daarin de volgende tabellen:

* `agencies` voor vervoerders;
* `stations` voor stations en dienstregelingspunten;
* `train_types` voor de treintypes;
* `train_series` voor de treinseries;
* `trains` voor de treinen.

### Vervoerders (`agencies`)

#### Attributen

Een vervoerder bevat de volgende attributen:

Naam | Type | Attribuut | Beschrijving
--- | --- | --- | ---
`name` | `string` | Verplicht | De naam van de vervoerder.
`abbr` | `string` | Optioneel | De afkorting van de vervoerder.
`desc` | `string` | Optioneel | Een beschrijving van de vervoerder.

#### Specificatie

Een vervoerder wordt op de volgende manier gespecificeerd, waarbij de id van de vervoerder achter `agencies.` geplaast wordt:

```toml
[agencies.ns]
name = "Nederlandse Spoorwegen"
```

Een collectie van vervoerders kan ook op een kortere manier worden gedefinieerd. De twee stijlen kunnen door elkaar gebruikt worden:

```toml
[agencies]
ns = {name = "Nederlandse Spoorwegen"}
db = {name = "Deutsche Bahn"}
```

### Stations en dienstregelingspunten (`stations`)

#### Attributen

Een station bevat de volgende attributen:

Naam | Type | Attribuut | Beschrijving
--- | --- | --- | ---
`name` | `string` | Verplicht | De naam van het station.
`short_name` | `string` | Optioneel | De korte naam van het station; indien leeg wordt de naam hiervoor gebruikt.
`desc` | `string` | Optioneel | Een beschrijving van het station.
`node` | `boolean` | Optioneel | Geeft aan of dit station een knooppuntstation is (`true`) of niet (`false`).
`x` | `float` | Optioneel | De x-coördinaat of de lengtegraad van het station.
`y` | `float` | Optioneel | De y-coördinaat of de breedtegraad van het station.

#### Specificatie

Een station wordt op de volgende manier gespecificeerd, waarbij de id van het station achter `stations.` geplaast wordt:

```toml
[stations.asd]
name = "Amsterdam Centraal"
short_name = "Amsterdam C"
node = true
x = 4.900556
y = 52.378889
```

Een collectie van stations kan ook op een kortere manier worden gedefinieerd. De twee stijlen kunnen door elkaar gebruikt worden:

```toml
[stations]
rtd = {name = "Rotterdam Centraal", node = true}
rtda = {name = "Rotterdam Alexander"}
```

### Treintypes (`train_types`)

#### Attributen

Een treintype bevat de volgende attributen:

Naam | Type | Attribuut | Beschrijving
--- | --- | --- | ---
`name` | `string` | Verplicht | De naam van het treintype.
`abbr` | `string` | Optioneel | De afkorting van het treintype.
`desc` | `string` | Optioneel | Een beschrijving van het treintype.

#### Specificatie

Een treintype wordt op de volgende manier gespecificeerd, waarbij de id van het treintype achter `train_types.` geplaast wordt:

```toml
[train_types.ic]
name = "Intercity"
abbr = "IC"
```

Een collectie van treintypes kan ook op een kortere manier worden gedefinieerd. De twee stijlen kunnen door elkaar gebruikt worden:

```toml
[train_types]
ic = {name = "Intercity", abbr = "IC"}
spr = {name = "Sprinter", abbr = "SPR"}
```

### Treinseries (`train_series`)

#### Attributen

Een treinserie bevat de volgende attributen:

Naam | Type | Attribuut | Beschrijving
--- | --- | --- | ---
`agency` | `string` | Verplicht | De id van de vervoerder van de treinserie.
`type` | `string` | Verplicht | De id van het treintype van de treinserie.
`name` | `string` | Verplicht | De naam van de treinserie.
`abbr` | `string` | Optioneel | De afkorting van de treinserie.
`desc` | `string` | Optioneel | De beschrijving van de treinserie.
`route` | `table` | Verplicht | De route van de treinserie.

De routetabel van een treinserie is een tabel van routepunten. Een routepunt bevat de volgende attributen:

Naam | Type | Attribuut | Beschrijving
--- | --- | --- | ---
`type` | `string` | Verplicht | Het type van het punt: `begin` voor een vertrekstation, `end` voor een aankomststation, `stop` voor een vertrek- en aankomststation, `pass` voor een station waar de trein alleen passeert.
`station` | `string` | Verplicht | De id van het station van het punt.
`platform` | `string` | Optioneel | Het spoor waarop de trein stopt.
`arr` | `string` | Verplicht/Optioneel | De tijd waarop de trein op dit station aankomt in de vorm `HH:MM`. Verplicht bij types `stop` en `end`.
`dep` | `string` | Verplicht/Optioneel | De tijd waarop de trein van dit station vertrekt in de vorm `HH:MM`. Verplicht bij types `begin` en `stop`.

#### Specificatie

Een treintype wordt op de volgende manier gespecificeerd, waarbij de id van het treintype achter `train_types.` geplaast wordt:

```toml
[train_series.500]
agency = "ns"
type = "IC"
name = "IC 500 Rotterdam Centraal - Leeuwarden"
abbr = "500"

[train_series.500.route]
0 = {type = 'begin', station = "rtd", dep = "00:05"}
1 = {type = 'stop', station = "rtda", arr = "00:12", dep = "00:13"}
2 = {type = 'stop', station = "gd", arr = "00:23", dep = "00:24"}
3 = {type = 'stop', station = "ut", arr = "00:42", dep = "00:49"}
4 = {type = 'stop', station = "amf", arr = "01:02", dep = "01:04"}
5 = {type = 'stop', station = "zl", arr = "01:39", dep = "01:45"}
6 = {type = 'stop', station = "asn", arr = "02:24", dep = "02:25"}
7 = {type = 'end', station = "gn", arr = "02:42"}
```

Het wordt niet aanbevolen om een verkorte versie voor het definiëren van treinseries te gebruiken.

### Treinen (`trains`)

#### Attributen

Een trein bevat de volgende attributen:

Naam | Type | Attribuut | Beschrijving
--- | --- | --- | ---
`series` | `string` | Verplicht | De id van de treinserie van deze trein.
`time` | `string` | Verplicht | De vertrektijd van deze trein in de vorm `HH:MM`. De vertrek- een aankomsttijden van de treinserie worden bij deze waarde opgeteld; een `time` van 07:00 met als `dep` van het eerste routepunt om 00:15 vertrekt dus daadwerkelijk om 07:15
`begin_at_point` | `string` | Optioneel | Indien gespecificeerd begint de trein bij het routepunt met deze id. Laat leeg om bij het begin van de route te beginnen.
`end_at_point` | `string` | Optioneel | Indien gespecificeerd eindigt de trein bij het routepunt met deze id. Laat leeg om bij het einde van de route te eindigen.
`agency` | `string` | Optioneel | De id van de vervoerder van de trein.
`type` | `string` | Optioneel | De id van het treintype van de trein.
`name` | `string` | Optioneel | De naam van de trein.
`abbr` | `string` | Optioneel | De afkorting van de trein.
`desc` | `string` | Optioneel | De beschrijving van de trein.

#### Specificatie

Een treintype wordt op de volgende manier gespecificeerd, waarbij de id van het treintype achter `train_types.` geplaast wordt:

```toml
[trains.531]
series = "500"
time = "09:00"
```

Een collectie van treinen kan ook op een kortere manier worden gedefinieerd. De twee stijlen kunnen door elkaar gebruikt worden:

```toml
[trains]
515 = {series = "500", time = "05:00", begin_at_point = "5"}
519 = {series = "500", time = "06:00"}
523 = {series = "500", time = "07:00"}
527 = {series = "500", time = "08:00"}
```
