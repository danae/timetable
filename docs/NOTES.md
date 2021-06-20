# Afspraken voor het gebruik van GATT in Garah

## Algemeen

* Zet voor elke id de drieletterige landcode van je land, bijvoorbeeld `tun_vrt` voor een vervoerder in Tunaran.

## Stations en dienstregelingspunten

* Voor `node` wordt `true` ingevuld indien een node het voorkeursstation is waar kan worden overgestapt voor andere richtingen. De reisplanner behandelt nodes met `node = true` als voorkeur voor overstappen.

## Treintypes

* Voor `priority` worden de volgende nummers aangehouden:

Prioriteit | Beschrijving
--- | ---
0 | Langeafstandstreinen die minder vaak stoppen dan intercity's
1 | Intercity's
2 | Sneltreinen, interregionale treinen
3 | Regionale treinen

## Treinseries

* Voor de id van een treinserie wordt `a` of `b` achter de daadwerkelijke id geplaatst om onderscheid te maken tussen resp. nominale of tegengestelde richting.
