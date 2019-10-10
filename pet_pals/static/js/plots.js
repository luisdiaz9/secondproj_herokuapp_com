var map = L.map('map').setView([19.436111,  -99.071944], 3);
function buildPlot1() {
    /* data route */
    var x1 = [], y1 = [];
    var x2 = [], y2 = []; 
    var x3 = [], y3 = [];
  var destination1 = d3.select(".destination1");
  var destination2 = d3.select(".destination2");
  var destination3 = d3.select(".destination3");
  var airline1 = d3.select(".airline1");  
  var airline2 = d3.select(".airline2");  
  var airline3 = d3.select(".airline3");  
  var dates1 = d3.select(".dates1");
  var dates2 = d3.select(".dates2");
  var dates3 = d3.select(".dates3");
  var url = "/api/pal";
  var airline_value1 = airline1.property("value");
  var airline_value2 = airline2.property("value");
  var airline_value3 = airline3.property("value");
  var dest_value1 = destination1.property("value");
  var dest_value2 = destination2.property("value");
  var dest_value3 = destination3.property("value");
  var dates_value1 = dates1.property("value");
  var dates_value2 = dates2.property("value");
  var dates_value3 = dates3.property("value");

  d3.json(url).then(function(response) {
  
  for (var i = 0; i < response[0]["name"].length ; i++) {
    row00 = response[0]["no"][i];
    row1 = response[0]["name"][i];
    row2 = response[0]["destino"][i];
    if(row00 === dates_value1 && row1 === airline_value1 && row2 === dest_value1){ 
        x1.push( response[0]["hora_salida"][i] );
        y1.push( response[0]["desde"][i]*response[0]["mxn"][i]);
        var line1 = L.polyline([[19.436111,  -99.071944], [19.436111,  -99.071944],[response[0]["lat"][i],response[0]["lon"][i]]]);
        map.addLayer(line1);
        var animatedMarker1 = L.animatedMarker(line1.getLatLngs());
        map.addLayer(animatedMarker1); 
          }
}

for (var i = 0; i < response[0]["name"].length ; i++) {
  row01 = response[0]["no"][i];
  row3 = response[0]["name"][i];
  row4 = response[0]["destino"][i];
  if(row01 === dates_value2 && row3 === airline_value2 && row4 === dest_value2){ 
      x2.push( response[0]["hora_salida"][i] );
      y2.push( response[0]["desde"][i]*response[0]["mxn"][i]);
      var line2 = L.polyline([[19.436111,  -99.071944], [19.436111,  -99.071944],[response[0]["lat"][i],response[0]["lon"][i]]]);
      map.addLayer(line2);
      var animatedMarker2 = L.animatedMarker(line2.getLatLngs());
      map.addLayer(animatedMarker2); 
        }
}

for (var i = 0; i < response[0]["name"].length ; i++) {
  row02 = response[0]["no"][i];
  row5 = response[0]["name"][i];
  row6 = response[0]["destino"][i];
  if(row02 === dates_value3 && row5 === airline_value3 && row6 === dest_value3){ 
      x3.push( response[0]["hora_salida"][i] );
      y3.push( response[0]["desde"][i]*response[0]["mxn"][i]);
      var line3 = L.polyline([[19.436111,  -99.071944], [19.436111,  -99.071944],[response[0]["lat"][i],response[0]["lon"][i]]]);
      map.addLayer(line3);
      var animatedMarker3 = L.animatedMarker(line3.getLatLngs());
      map.addLayer(animatedMarker3); 
        }
}


    // Create the Traces
var trace1 = {
  x: x1,
  y: y1,
  mode: "line",
  type: "scatter",
  name: airline_value1 + " " + dest_value1 + " " + dates_value1,
  marker: {
    color: "#2077b4",
    symbol: "hexagram"
  }
};

var trace2 = {
  x: x2,
  y: y2,
  mode: "markers",
  type: "scatter",
  name: airline_value2 + " " + dest_value2 + " " + dates_value2,
  marker: {
    color: "orange",
    symbol: "diamond-x"
  }
};

var trace3 = {
  x: x3,
  y: y3,
  mode: "markers",
  type: "scatter",
  name: airline_value3 + " " + dest_value3 + " " + dates_value3,
  marker: {
    color: "#b42020",
    symbol: "cross"
  }
};

// Create the data array for the plot
var data = [trace1, trace2, trace3];

// Define the plot layout
var layout = {
  autosize: true,

  title: airline1.value,
  xaxis: { 
title: "",
tickformat: '%Y-%m-%d',
    type: 'category', 
automargin: true

 },
  yaxis: { title: "($) MXN", type: "linear", automargin: true }
};


    Plotly.newPlot("plot2", data, layout);
  

  //debugger
 
  L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    subdomains: ['a','b','c']
})
  .addTo(map);



});

}

buildPlot1();



function buildPlot() {
  /* data route */
var url = "/api/pals";
d3.json(url).then(function(response) {

  console.log(response);

  var data = response;

  var layout = {

    title: "Destinations",
    showlegend: false,
    height: 600,
          // width: 980,
        
    geo: {

      projection: {
        type: "robinson"
      },
      showland: true,
      landcolor: "rgb(217, 217, 217)",
      subunitwidth: 1,
      countrywidth: 1,
      subunitcolor: "rgb(255,255,255)",
      countrycolor: "rgb(255,255,255)"
    }
  };

  Plotly.newPlot("plot", data, layout);
});
}

buildPlot();

