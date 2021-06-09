let topics = JSON.parse(document.getElementById("trends-data").textContent);
topics = topics.filter((topic) => !!topic.tweet_volume)
topics.forEach((topic) => topic.name = topic.name.replace("#", ""));

am4core.useTheme(am4themes_animated);

am4core.useTheme(am4themes_animated);
var chart = am4core.create("chartdiv", am4plugins_wordCloud.WordCloud);
var series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());

series.data = topics;

series.dataFields.word = "name";
console.log(Object.keys(series.dataFields));
series.dataFields.value = "tweet_volume";

series.colors = new am4core.ColorSet();
series.colors.passOptions = {};


//todo: aggiungere il link alla pagina twitter
series.labels.template.url = "http://www.twitter.com/search?q={word}";
series.labels.template.urlTarget = "_blank";