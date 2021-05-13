const ws_max = [6.61666667, 35.48333333]
const en_max = [18.51666667, 47.08333333]
let data, map, request_format
let markers = []

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

function makeMap(c) {
    const center = JSON.parse(c)

    const delta = 1.59275 * Math.PI / 180

    const ws = [center[0] - delta, center[1] - delta];
    const en = [center[0] + delta, center[1] + delta];

    map = new mapboxgl.Map({
        container: document.getElementById('map'),
        //custom style
        style: 'mapbox://styles/andter99/ckodi69160sje17p7inup5501',
        center: center,
        zoom: 10,
        bounds: [ws, en],
        maxBounds: [ws_max, en_max],
    });

    map.addControl(new mapboxgl.NavigationControl(), 'top-left')
    map.addControl(new mapboxgl.ScaleControl())
    map.addControl(new SearchControl(), 'top-right')

    map.on('movestart', function () {
        let btn = document.getElementById("map-search-btn")
        btn.disabled = true
    });
    map.on('moveend', function () {
        let btn = document.getElementById("map-search-btn")
        btn.disabled = false
    });

    getData({
        lng: center[0],
        lat: center[1]
    })
}

function searchBtnClicked() {
    let btn = document.getElementById("map-search-btn")
    btn.disabled = true

    getData()
}

function onDownloadClicked() {
    let center = map.getCenter()

    downloadMapData({"data": data}, [center.lng, center.lat])
}

async function getData() {
    const center = map.getCenter()
    const long = center.lng
    const lat = center.lat
    const rad = 4 //dubito che abbia senso uno diverso

    try {
        const response = await fetch(request_format.format(lat, long, rad))
        const stats = (await response.json()).statuses

        //Filtraggio dei dati ricevuti da twitter
        data = []
        stats.forEach((s) => {
            let c = s.coordinates
            data.push({
                "id_str": s.id_str,
                "created_at": s.created_at,
                "coords": `${(c != null) ? JSON.stringify(c.coordinates) : null}`,
                "lang": `${(s.lang !== "und") ? s.lang : null}`,
                "text": s.text,
                "user_id": s.user.id_str,
                "user_name": s.user.name,
                "user_scrn_name": s.user.screen_name
            })
        })

        let filler = document.getElementById("galangalo")
        if (filler != null) {
            document.removeChild(filler)
        }

        let column = document.getElementById("map-results")
        while (column.hasChildNodes()) {
            column.removeChild(column.lastChild);
        }

        markers.forEach((m) => m.remove())

        if (data.length > 0) {
            data.forEach((d) => {
                let c = JSON.parse(d.coords)
                if (c != null) {
                    // create a HTML element for each feature
                    let el = document.createElement('div')
                    el.className = "tweet-marker"

                    // make a marker for each feature and add to the map
                    markers.push(new mapboxgl.Marker(el).setLngLat(c).addTo(map))
                }

                let row = document.createElement("div")
                row.className = "row"
                row.textContent = d.text
                column.append(row)
            })
        } else {
            let row = document.createElement("div")
            row.className = "row alert alert-danger"
            row.textContent = "Nessun tweet trovato nella zona"
            column.append(row)
        }
    } catch (e) {
        console.error(e)
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