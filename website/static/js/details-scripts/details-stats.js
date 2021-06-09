var tweets_d = JSON.parse(document.getElementById("tweets-data").textContent);

const millisecToHours = 1 / (60 * 60 * 1000)

//Numero totale dei tweet per la ricerca
let tweets_count = tweets_d.length;

//Numero dei tweet contenenti immagini
let media = tweets_d.filter((tweet) => !!tweet && !!tweet.entities && !!tweet.entities.media)
let images_number = parseInt(media.length, 10);

//Numero dei tweet geolocalizzati
let geolocalizzati = tweets_d.filter((tweet) => !!tweet.geo || !!tweet.place || !!tweet.coordinates );

let is_geo = parseInt(geolocalizzati.length, 10);
let tweets_number = parseInt(tweets_count, 10);
//Percentuale di tweet geolocalizzati
let percentuale = parseInt((is_geo * 100) / tweets_number);

//Media oraria
function getHourlyAverage() {
    let first = new Date(tweets_d[0].created_at)
    let last = new Date(tweets_d[tweets_d.length - 1].created_at)

    let diffHours = millisecToHours * Math.abs(first - last)

    if (diffHours === 0)
        return 0

    return (tweets_count / diffHours).toFixed(4)
}

function getTweetsNumber() {
    return tweets_number;
}

function getImagesNumber() {
    return images_number;
}

function getIs_geo() {
    return is_geo;
}

function getPercentuale() {
    return percentuale;
}

function getMediaPubblicazione() {
    let hSum = 0
    let mSum = 0
    let sSum = 0
    tweets_d.forEach((tweet) => {
        let d = new Date(tweet.created_at)
        hSum += d.getUTCHours() / tweets_count
        mSum += d.getUTCMinutes() / tweets_count
        sSum += d.getUTCSeconds() / tweets_count
    })

    return [hSum, mSum, sSum].map((s) => Math.floor(s)).join(":")
}

function returnText() {
    return `Numero totale di tweet trovati per ${tag}${hasher}: ${tweets_number};\n` +
        `Numero dei tweet che contengono immagini: ${images_number};\n` +
        `Numero dei tweet geolocalizzati: ${is_geo}\n` +
        `Percentuale dei tweet geolocalizzati: ${percentuale}%;\n` +
        `Media Oraria: ${getHourlyAverage()};\n` +
        `Orario medio di pubblicazione: ${getMediaPubblicazione()}`

}


// bar chart
const data = {
    labels: [
        'Totale tweet trovati',
        'Con immagine',
        'Geolocalizzati',
      ],
    datasets: [{
        label: 'Statistiche',
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)'
        ],
        hoverOffset: 4,
        radius: 300,
        data: [ getTweetsNumber(), getImagesNumber(), getIs_geo() ],
    }]
};

const config = {
     type: 'bar',
     data: data,
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
};

var myChart = new Chart(
    document.getElementById('myChart'),
    config
);


//text
document.getElementById("perc-loc").textContent = `${percentuale}%`;
document.getElementById("med-or").textContent = `${getHourlyAverage()}tw/h`;
document.getElementById("ora-pub").textContent = `${getMediaPubblicazione()}`;
