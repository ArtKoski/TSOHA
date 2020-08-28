## ProgressTracker

https://tsoha-progresstracker.herokuapp.com/

Verkkosivu on luotu treenitulosten säilömiseen. 
Käytännön esimerkki:  
Henkilö haluaa kehittyä leuanvedossa ja säilöä treenituloksensa johonkin.
ProgressTrackerin avulla hän valitsee leuanvedon 'seurattavaksi liikeeksi' 
(=tracked exercise), jonka jälkeen hän pystyy tallentamaan treenituloksia 
aina treenien yhteydessä. Esim: ekana päivänä 3x5, 0 kg, Kolmantena päivänä 
5x5, 0 kg, tokana viikkona 3x5, 5kg jne.  

Toiminnallisuudet ovat:
  
Käyttäjätunnuksen luominen, sisäänkirjautuminen
Treeniliikkeiden valinta, eli valitaan mitä liikkeitä halutaan 'seurata'.
Treeniliikkeille on oma tietokanta, josta liikkeitä voi hakea. 
Jos liikettä ei löydy, sen pystyy lisäämään itse käyttäjä. Todellisessa palvelussa
tämä tarvitsisi jonkinlaista filtteriä tai liikkeiden lisäyksen hoitaisi admin, 
mutta tässä sovelluksessa kuka tahansa pystyy lisäämään minkä tahansa nimisiä 
liikkeitä tietokantaan.
Treenien tallentaminen formaatilla 'sarjat, toistot, paino(kg) ja lisätiedot'  
Tallenetun treenin editointi sekä poistaminen
Tallennettujen treenien filtteröinti, eli kuinka monta treeniä näkyy sivulla.


Toiminnallisuudet jotka jäivät tekemättä:  
-Treenien yhteenveto: tarkoitus oli tehdä kuvaaja, josta näkisi kehitystä pohjautuen tallennetuihin treeneihin.
Tämä kuitenkin osoittautui hyvin hankalaksi kokemukseeni nähden (olisi vaatinut hieman javascriptin osaamista sekä
chart.js-käyttöä, joihin en enää ehtinyt perehtyä)
-Suunnitelmissa oli myös mahdollinen foorumi tai jonkinlainen treenin jakaminen muille käyttäjille, mutta niiden sijaan
käytin aikani valmiina olevien ominaisuuksien parantamiseen.




