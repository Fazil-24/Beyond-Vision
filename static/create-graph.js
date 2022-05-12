/*
 * Parse the data and create a graph with the data.
 */
function parseData(createGraph) {
	Papa.parse("static/crowd_data.csv", {
		download: true,
		complete: function(results) {
			createGraph(results.data);
		}
	});
}

function createGraph(data) {
	var years = [];
	var hcount = ["Human count"];

	for (var i = 1; i < data.length; i++) {
		
		if (data[i][1] !== undefined  && data[i][1] !== undefined ) {
			years.push(data[i][0]);
			hcount.push(data[i][1]);
		}
		else {
			// push 0 to signify no data
			years.push(0);
			hcount.push(0)
		}
		
	}


	var chart = c3.generate({
		bindto: '#chart',
	    data: {
	        columns: [
	        	hcount
	        ]
	    },
	    axis: {
	        x: {
	            type: 'category',
	            categories: years,
				label: 'Time',  
	        },
			y: {
				label: 'Crowd'
			},
	    },
	    zoom: {
        	enabled: true
    	}
	});
}

parseData(createGraph);