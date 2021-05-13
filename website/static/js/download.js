tags = {
    "@" : "user",
    "#" : "hashtag",
    "tr" : "trends",
    "mp" : "map"
}

function downloadMapData(data, coords) {
    downloadData(data, "mp", `${coords[1]}N-${coords[0]}E`)
}

function downloadTrendsData(data, count=50) {
    downloadData(data, "tr", `top-${count}`)
}

function downloadData(json_data, tag, name) {
    tweets = JSON.parse(json_data)
    const fields = Object.keys(tweets[0])

    const type = tags[tag]
    const csv = [
        fields.join(','),
        tweets.map(row =>
            fields.map(fieldName => JSON.stringify(row[fieldName])).join(',')
        ).join('\n')
    ].join('\n')

    const date = new Date()
    const date_stamp = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
    const time_stamp = `${date.getHours()}-${date.getMinutes()}-${date.getSeconds()}`
    const fileName = `${type}_${name}_${time_stamp}_${date_stamp}.csv`
    const fileBlob = new Blob([csv], {type: "text/plain;charset=utf-8"});

    saveAs(fileBlob, fileName);
}