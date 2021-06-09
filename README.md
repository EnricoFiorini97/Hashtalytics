### Descrizione della soluzione proposta

Interfaccia web per l’analisi di tweet raccolti per rilevare gli hashtag in tendenza.
Il prodotto verrà utilizzato dai dipendenti dell’azienda e dal titolare, per analisi di mercato e tendenze da sfruttare per eventuali campagne pubblicitarie a favore dell’azienda
L’applicativo permette di visualizzare una mappa con i punti di interesse (tramite segnalini/simboli) che rappresentano eventi o emergenze.
E’ possibile ricercare tramite una barra degli indirizzi situata in alto del sito una specifica area geografica (comprendente solo il territorio italiano).
Dal menu si può selezionare la sezione dedicata alle tendenze con i link dei vari alert che rimandano al tracciamento dell’hashtag scelto con le varie analisi. 
Per limitare l’accesso ad utenti non autorizzati è prevista una sezione per il login.
Qui sotto vengono elencate le varie voci che saranno disponibili.


- **TRENDING**: Home page con info sui tweet dell’ultima ora/giorno/settimana (selezionabile in una tendina), il primo elemento che appare è una “term cloud” con tutti gli hashtag più di tendenza nella finestra temporale selezionata. La seconda cosa che appare è una mappa dell’italia che si può visitare tipo un embed di google maps (o mapbox, o simili) che mostra dei tweet geolocalizzati che sono in tendenza in base alla zona che si sta visualizzando.
Ogni hashtag è un link alla pagina dedicata hashtag  (esempio www.sito.com/hashtag?tag=deltaplano)
In questa sezione sarà presente la possibilità di vedere gli “allarmi”, ovvero gli hashtag di tendenza più ricercati. 


- **HASHTAG**: una sezione che analizza un determinato hashtag, se non gli viene fornito nella richiesta (?tag=elefante) allora propone dei suggerimenti random dei tweet più frequenti e fornisce una barra di ricerca dove specificare l’hashtag (se non si vuole scegliere uno dei suggerimenti).
Una volta selezionato un hashtag vengono visualizzate varie statistiche. 
Alcune possibilità potrebbero essere:
un grafico temporale (tipo quello del valore delle azioni nel tempo) che mette in mostra il numero di tweet giornalieri nel tempo (quindi ad esempio da la possibilità di vedere quanto un tweet è stato utilizzato nell’ultimo giorno/mese/anno ecc…)
una mappa che fa vedere i posti dove l’hashtag viene utilizzato più frequentemente
una breve lista di tweet (di oggi, dell’ultimo mese, etc) più popolari che contengono quell’hashtag
una lista o una term cloud con tutti gli hashtag più utilizzati assieme all’hashtag selezionato

- **TIMELINE**: una sezione che analizza i tweet di un utente in ordine cronologico e spaziale: si crea una mappa e si piazzano tutti i tweet della persona come dei pin, che poi vengono sequenzialmente collegati da una riga.

Per ogni hashtag o persona sarà possibile scaricare i dati relativi nei formati più diffusi.
