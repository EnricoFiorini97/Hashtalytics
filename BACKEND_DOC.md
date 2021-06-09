## Backend Developing Team

### Membri

| Nome | Matricola | Ruolo |
| ------ | ------ | ------ |
| Enrico Fiorini | 128426 | Developer-Backend-SYS OP |
| Carmine La Luna | 131015 | Developer-Backend-SYS OP |


### Descrizione degli endpoint esposti dalle API

Di seguito verranno esposti esempi di chiamate via URL al backend con relativi parametri querizzati:

- **FETCHARE TWEET DI UN UTENTE**: La chiamata si occupa di filtrare e fetchare gli ultimi 10 tweets di un utente.
I campi contenuti nel JSON di risposta sono i seguenti: id, author_id, text.

Esempio URL chiamata all'endpoint: /twapi/user/<nome_user>


- **FETCHARE UN HASHTAG**: La chiamata si occupa di filtrare e fetchare gli ultimi 15 hashtags corrispondenti alla ricerca effettuata.
I campi contenuti nel JSON di risposta sono i seguenti: id, author_id, text, created_at.

Esempio URL chiamata all'endpoint: /twapi/hashtag/<nome_hashtag>


- **FETCHARE TRENDS DI UNA NAZIONE**: La chiamata si occupa di filtrare e fetchare i top 50 hashtags in tendenza nella nazione corrispondente alla ricerca effettuata.
I campi contenuti nel JSON di risposta sono i seguenti: name, url, text, trends_volume. NB: L'id per fetchare gli hashtags in tendenza in Italia corrisponde a 23424853.

Esempio URL chiamata all'endpoint: /twapi/trends/


- **FETCHARE TRENDS DA COORDINATE**: La chiamata si occupa di filtrare e fetchare fino a 100 hashtags corrispondenti ad una circonferenza centrata in latidudine e longitudine di raggio x kilometri.
I campi contenuti nel JSON di risposta sono i seguenti: id, created_at, text, name, screen_name.

Esempio URL chiamata all'endpoint: /twapi/location/<latitudine>/<longitudine>/<raggio>

### Cronjobs

- **DB DATA STORAGE**: Il cronjob si occupa di immagazzinare ciclicamente nel DB i dati relativi ai trends, a distanza di un lasso di tempo pari a 1 ora. I dati immagazzinati relativi ai trends vengono utilizzati per estrarre gli hashtag associati, che vengono a loro volta immagazzinati sottoforma di hashtag collegati a tweets.