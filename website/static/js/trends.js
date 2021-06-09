let topics = JSON.parse(document.getElementById("trends-data").textContent);
console.log(Object.keys(topics))

topics = topics.filter((topic) => !!topic.tweet_volume)

let labels = topics.map((topic) => {
    return topic.name
})

const data = {
    labels: labels,
    datasets: [{
        label: 'Top Trends',
        data:
            topics.map((topic) => {
                return topic.tweet_volume ? topic.tweet_volume : 0
            })
        ,
        backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
        ],
        borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
        ],
        borderWidth: 1
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
    }
};
// === include 'setup' then 'config' above ===

var myChart = new Chart(
    document.getElementById('myChart'),
    config
);
