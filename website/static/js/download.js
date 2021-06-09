const tags = {
    "@" : "user",
    "#" : "hashtag",
    "tr" : "trends",
    "mp" : "map"
}

function downloadMapData(data, coords) {
    downloadData(JSON.stringify(data.data), "mp", `${coords[1]}N-${coords[0]}E`)
}

function downloadTrendsData(data, count=50) {
    downloadData(data, "tr", `top-${count}`)
}

function downloadDetailsData(raw_data, tag, name) {
    const tweets = JSON.parse(raw_data)

    //Filtraggio dei dati ricevuti da twitter
    let data = []
    tweets.forEach((s) => {
        data.push({
            "created_at": s.created_at,
            "favorite_count": s.favorite_count,
            "retweet_count": s.retweet_count,
            "id_str": s.id_str,
            "lang": `${(s.lang !== "und") ? s.lang : null}`,
            "text": s.text,
            "user_id": s.user.id_str,
            "user_name": s.user.name,
            "user_scrn_name": s.user.screen_name,
            "user_verified": s.user.verified
        })
    })

    console.log(data)

    downloadData(JSON.stringify(data), tag, name)
}

function downloadData(json_data, tag, name) {
    const tweets = JSON.parse(json_data)
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