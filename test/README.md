## Test

Questa sezione contiene il codice di test di unità (TDD, TL), descrizione test di integrazione e accettazione se non integrati nell’IDE

Per testare la soluzione in locale è necessario farla partire con
```bahs
python manage.py runserver
```
E in un altro terminale avviare il test
```bahs
python manage.py test test
```

### Nota
Per far partire la soluzione in locale è necessario:

- un virtual env di python
- pipenv
- l'installazione dei moduli aggiuntivi (`pipenv install`)
- un file `env.py` creato seguendo le istruzioni presenti nel file `env-sample.py`
