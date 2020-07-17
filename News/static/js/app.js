
function loadDropDown(dropPick, columns, defaultOptionName) {
    // Support function to used to load drop down 
    let selectOpt = d3.select(dropPick);
    let options = selectOpt.selectAll("option")
        .data(columns)
        .enter()
        .append("option")
        .attr("value", function(d) {
            return d;
        })
        .text(function(d) {
            return d;
        });
    options.property("selected", function(d) { return d === defaultOptionName })

}


function buildUrl(url, parameters){
    var qs = "";
    for(var key in parameters) {
      var value = parameters[key];
      qs += encodeURIComponent(key) + "=" + encodeURIComponent(value) + "&";
    }
    if (qs.length > 0){
      qs = qs.substring(0, qs.length-1); //chop off last "&"
      url = url + "?" + qs;
    }
    return url;
  }

  function tabulate(data, columns) {
    var table = d3.select('#contNews').append('table')
    var thead = table.append('thead')
    var	tbody = table.append('tbody');

    // append the header row
    thead.append('tr')
      .selectAll('th')
      .data(columns).enter()
      .append('th')
        .text(function (column) { return column; });

    // create a row for each object in the data
    var rows = tbody.selectAll('tr')
      .data(data)
      .enter()
      .append('tr');

    // create a cell in each row for each column
    var cells = rows.selectAll('td')
      .data(function (row) {
        return columns.map(function (column) {
          return {column: column, value: row[column]};
        });
      })
      .enter()
      .append('td')
        .text(function (d) { return d.value; });

  return table;
}


async function getnews()
{
    selectedDate = d3.select("#selDate").node().value;
    selectedCategory = d3.select("#selCategory").node().value;
    selectedSentiment = d3.select("#selSentiment").node().value;
    selectedLimit = d3.select("#selLimit").node().value;

    const parameters={
        'date':selectedDate,
        'category':selectedCategory.toLowerCase() ,
        'sentiment':selectedSentiment,
        'limit':selectedLimit
    }
    //const url = '/news_data/?date=${selectedDate}&category=${selectedCategory}&sentiment=${selectedSentiment}';
    const url = buildUrl('/news_data/',parameters);
    newsdata = await d3.json(url);

    tabulate(newsdata,['title','url'])

    

}

function loadSentiment() {
    // Load theYears dropdown
    let columns = ['Positive', 'Neutral', 'Negative']
    loadDropDown('#selSentiment', columns, columns[0])
}

function loadLimit() {
    // Load theYears dropdown
    let columns = ['10', '20', '50']
    loadDropDown('#selLimit', columns, columns[0])
}


function loadCategories() {
    // Load theYears dropdown
    let columns = ['Business','Entertainment','General','Health','Science','Sports','Technology']
    loadDropDown('#selCategory', columns, columns[0])
}

function loadnewsDates(newsdates) {
    // Load theYears dropdown
    function strDes(a, b) {
        if (a>b) return -1;
        else if (a<b) return 1;
        else return 0;
      }    
    let columns = []
    newsdates.forEach(element => {
        columns.push(element.date)
    });
    columns.sort(strDes);
    loadDropDown('#selDate', columns, columns[0])

}


async function init() {
    // Load the Census and Unemployement data

    const url = "/news_dates/"
    newsdates = await d3.json(url);
    loadSentiment();
    loadCategories();
    loadLimit();
    loadnewsDates(newsdates);
}

init();

