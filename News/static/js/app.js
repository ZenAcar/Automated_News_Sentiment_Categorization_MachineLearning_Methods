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


function buildUrl(url, parameters) {
    var qs = "";
    for (var key in parameters) {
        var value = parameters[key];
        qs += encodeURIComponent(key) + "=" + encodeURIComponent(value) + "&";
    }
    if (qs.length > 0) {
        qs = qs.substring(0, qs.length - 1); //chop off last "&"
        url = url + "?" + qs;
    }
    return url;
}


function generateDynamicTable(data, columns,headers){
	
    var noOfRecords = data.length;
    
    if(noOfRecords>0){
        // CREATE DYNAMIC TABLE.
        d3.select('#contNews').selectAll("table").remove(); // Only remove tables under conNews
        var table = document.createElement("table");        
        table.style.width = '80%';
        table.setAttribute('border', '1');
        table.setAttribute('cellspacing', '0');
        table.setAttribute('cellpadding', '5');
      
        // CREATE TABLE HEAD .
        var tHead = document.createElement("thead");	
        // CREATE ROW FOR TABLE HEAD .
        var hRow = document.createElement("tr");
        
        // ADD COLUMN HEADER TO ROW OF TABLE HEAD.
        for (var i = 0; i < headers.length; i++) {
                var th = document.createElement("th");
                if (i < headers.length -1){
                th.setAttribute('width','45%')
                }
                else{
                    th.setAttribute('width','10%')
                }
                th.innerHTML = headers[i];
                hRow.appendChild(th);
        }
        tHead.appendChild(hRow);
        table.appendChild(tHead);		
		// CREATE TABLE BODY .
        var tBody = document.createElement("tbody");	
        for (var i = 0; i < noOfRecords; i++) {
        
                var bRow = document.createElement("tr"); // CREATE ROW FOR EACH RECORD .
                for (var j = 0; j < columns.length; j++) {
                    var td = document.createElement("td");
                    let cell_content=''
                    if (j ==0 ){
                        cell_content = '<a href="' + data[i]['url']+'">'+data[i][columns[j]]+'</a>' ;
                    }
                    else
                    {
                        cell_content=data[i][columns[j]];
                    }
                    td.innerHTML = cell_content;
                    bRow.appendChild(td);
                }
                tBody.appendChild(bRow)
        }
        table.appendChild(tBody);	
        // // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
        // var divContainer = document.getElementById("myContacts");
        var divContainer = d3.select('#contNews').node()
         divContainer.innerHTML = "";
         divContainer.appendChild(table);
        
    }	
}

async function getnews() {
    selectedDate = d3.select("#selDate").node().value;
    selectedCategory = d3.select("#selCategory").node().value;
    selectedSentiment = d3.select("#selSentiment").node().value;
    selectedLimit = d3.select("#selLimit").node().value;

    const parameters = {
        'date': selectedDate,
        'category': selectedCategory.toLowerCase(),
        'sentiment': selectedSentiment,
        'limit': selectedLimit
    }
    console.log(parameters)
        //const url = '/news_data/?date=${selectedDate}&category=${selectedCategory}&sentiment=${selectedSentiment}';
    const url = buildUrl('/news_data/', parameters);
    newsdata = await d3.json(url);

    generateDynamicTable(newsdata, ['title',  'summary', 'source'],['Title','Article Summary','Source'])

    // tabulate(newsdata, ['title',  'summary', 'source'])



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
    let columns = ['Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology']
    loadDropDown('#selCategory', columns, columns[0])
}

function loadnewsDates(newsdates) {
    // Load theYears dropdown
    function strDes(a, b) {
        if (a > b) return -1;
        else if (a < b) return 1;
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