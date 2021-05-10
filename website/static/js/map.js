const rome = [12.534216244956292, 41.7409352435425]
const deltaLong = 7.5;
const deltaLat = 5.8;

const ws_max = [rome[0] - deltaLong, rome[1] - deltaLat];
const en_max = [rome[0] + deltaLong, rome[1] + deltaLat];
let data, map, request_format;

class SearchControl {
    onAdd(map) {
        this.map = map
        this.container = document.createElement('button')
        this.container.id = "map-search-btn"
        this.container.className = 'mapboxgl-ctrl btn btn-primary btn-lg'
        this.container.textContent = 'Cerca qui'
        this.container.onclick = searchBtnClicked
        this.container.disabled = true
        return this.container
    }

    onRemove() {
        this.container.parentNode.removeChild(this.container)
        this.map = undefined
    }
}

function makeMap(c, token) {
    mapboxgl.accessToken = token
    const center = JSON.parse(c)

    const delta = 1.59275 * Math.PI / 180

    const ws = [center[0] - delta, center[1] - delta];
    const en = [center[0] + delta, center[1] + delta];

    map = new mapboxgl.Map({
        container: 'map',
        //custom style
        style: 'mapbox://styles/andter99/ckodi69160sje17p7inup5501',
        center: center,
        zoom: 10,
        bounds: [ws, en],
        maxBounds: [ws_max, en_max],
    });

    getData({
        lng: center[0],
        lat: center[1]
    })

    map.addControl(new mapboxgl.NavigationControl(), 'top-left')
    map.addControl(new mapboxgl.ScaleControl())
    map.addControl(new SearchControl(), 'top-right')

    map.on('load', () => {
        //things to do after map is loaded

        // add markers to map - SARÀ UTILE IN FUTURO
        /*points.forEach(function (p) {
            // create a HTML element for each feature
            var el = document.createElement('div');
            el.className = "tweet-marker"

            // make a marker for each feature and add to the map
            new mapboxgl.Marker(el)
                .setLngLat(p)
                .addTo(map);
        });*/
    })
    map.on('movestart', function () {
        let btn = document.getElementById("map-search-btn")
        btn.disabled = true
    });
    map.on('moveend', function () {
        let btn = document.getElementById("map-search-btn")
        btn.disabled = false
    });
}

function searchBtnClicked() {
    let btn = document.getElementById("map-search-btn")
    btn.disabled = true

    getData()
}

function onDownloadClicked() {
    const center = map.getCenter()

    console.log(center)

    const obj = {
        "data" : data
    }

    console.log(obj)

    //FIXME: Al momento è improponibile scaricare a rudo i dati ottenuti da Twitter in quanto contorti
    console.log("tiscatusca")

    //downloadMapData(obj, center)
}

async function getData() {
    const center = map.getCenter()
    const long = center.lng
    const lat = center.lat
    const rad = 4 //dubito che abbia senso uno diverso

    try {
        const response = await fetch(request_format.format(lat, long, rad))
        data = (await response.json()).statuses

        let column = document.getElementById("map-results")

        while (column.hasChildNodes()) {
            column.removeChild(column.lastChild);
        }

        if (data.length > 0) {
            data.forEach((stat) => {
                let row = document.createElement("div")
                row.className = "row"
                row.textContent = stat.text
                column.append(row)
            })
        } else {
            let row = document.createElement("div")
            row.className = "row alert alert-danger"
            row.textContent = "Nessun tweet trovato nella zona"
            column.append(row)
        }
    } catch (e) {
        console.log("ops")
    }
}

if (!String.prototype.format) {
    String.prototype.format = function () {
        const args = arguments;
        return this.replace(/{(\d+)}/g, (match, number) => {
            return (typeof args[number] != 'undefined') ? args[number] : match
        })
    }
}