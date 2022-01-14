# Inlämningsuppgift i plattformar för AI-utveckling
Detta projekt är tänkt som inlämningsuppgift för kursen _Plattformar för AI-utveckling_ och inkluderar:
- En REST backend ([Flask](https://flask.palletsprojects.com/en/2.0.x/)) som tar in en text, räkna användningsfrekvensen av varje ord ([Spacy](https://spacy.io/)) och sparar den i en databas ([MongoDB](https://www.mongodb.com/)).  Ytterligare REST endpoints finns för hämtninng av den originala texten samt uppräknat ordfrekvensen.

- En frontend app ([Panel](https://panel.holoviz.org/)) for att interagera med REST API:n (med [requests]()) och visualusera ordfrekvensen som en Wordcloud ([word_cloud](https://amueller.github.io/word_cloud/)) och en bar chart ([Bokeh](https://bokeh.org/))

## Konsekvensanalys
### Övergripande arkitektur
Första beslut var kring övergripande arkitektur: applikationen är i nuläge väldigt liten, och det finns egentligen ingen riktig behöv att ha en renodlad uppdelning mellan backend och en frontend: de flesta Python frameworks tillåter ju att ha en lite UI direkt i servern och/eller integrera en REST API i UI.  
Den delade arkitekturen hade dock tydliga fordelar, bland annat:
- Vid tidsbrist, hade jag kunnat leverera endast en backend och andå få godkänt betyg
- Den gav möjligheter att testa flera frameworks & bibliotek, vilket är ju bra för en kurs
- Man skulle lätt kunna skala upp & expandera appen om man nu kände sig för det

### Backend
#### Flask vs Sanic vs annat
Då jag hade beslutat över att ha en backend + frontend arkitektur, det kändes rymlig att använda en "microframework" som Flask eller Sanic istället för något större (som Django).  
Benjamin ser utt att föredra Sanic, som verkar vara en modernare version av Flask med support för async förfrågor, men Flask ser ut att vara mer eller mindre en "industry standard" supporterad overallt och med massa tutorials på nätet.  
Eftersom jag inte var särkilt interesserad i async forfrågor och liknande (har inte en programmeringsbakgrund och har knapp kodat något async förut) bestämde jag mig för att köra med Flask.  

#### SQL vs NoSQL vs ingen DB alls
Jag hade ingen speciell anledning att spara data i min lilla app, och det skulle gå att ha en fungerande version utan någon databas alls, men då hade jag inte fått lära mig något.  
Min data passade inte speciellt bra till en SQL databas (varje text har ju olika antal ord och så har ordfrekvensen) och jag var nyfiken på att prova NoSQL, så jag skapade en MongoDB Atlas: det tog en lite stund att förstå hur man hämntar & manipulera data då jag var helt nybörjare, men dokumentationen är helt ok och det finns gått om exempel.

### Frontend
#### JavaScript vs Python frontend
Under kursen gick Jonathan genom hur man skapar frontend i JS med React eller Vue, vilket är vanligast i riktiga projekt.  
Dock har jag ingen tidigare erfarenhet av JS, CSS eller dylikt, och det kändes som att det var ganska mycket att ta in & läsa på för att bygga en enkel UI, speciellt om man vill integrera någon form av datavisualisering (diagrammer eller dylikt).  
Det kändes då lite enklare att hitta en "pure Python" lösning, där UI:t går att koda i Python.  
Jag har dock byggt enklare UI & dashboards i Python med Bokeh, och då kändes det som ett bra tillfälle för att testa Panel (som är baserad på Bokeh, men med fokus på att bygga just enkla appar).  
Panel (och Bokeh) är i sig baserad på en server-client arkitektur (Python servern skapar & upppdaterar JavaScript i browsern)