// Load data from JSON file
var data = [];
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
	if (xhr.readyState === XMLHttpRequest.DONE) {
		if (xhr.status === 200) {
			// Parse JSON data
			data = xhr.responseText.trim().split('\n').map(function(line) {
				return JSON.parse(line);
			});

			// Populate table with data
			var tbody = document.querySelector('#data-table tbody');
			data.forEach(function(row) {
				var tr = document.createElement('tr');
                /*
				<th>Title</th>
				<th>Description</th>
				<th>Grade</th>
				<th>Quality</th>
				<th>Height</th>
				<th>Notes</th>
				<th>Link</th>
                 *
                 * */
				tr.innerHTML = '<td>' + row.title + '</td>' +
				               '<td>' + row.description + '</td>' +
				               '<td>' + row.grade + '</td>' +
				               '<td>' + row.quality + '</td>' +
				               '<td>' + row.height + '</td>' +
				               '<td>' + row.notes + '</td>' +
				               '<td>' + row.link + '</td>';
				tbody.appendChild(tr);
			});
		} else {
			console.error(xhr.statusText);
		}
	}
};
xhr.open('GET', 'climbs.ndjson');
xhr.send();

// Search for matching data
var searchBox = document.querySelector('#search-box');
searchBox.addEventListener('input', function() {
	var searchTerm = searchBox.value;
	var options = {
		keys: ['title', 'description', 'grade', 'quality', 'height', 'notes', 'link'],
		includeScore: true,
		threshold: 0.4
	};
	var fuse = new Fuse(data, options);
	var results = fuse.search(searchTerm);
	var tbody = document.querySelector('#data-table tbody');
	tbody.innerHTML = '';
	results.forEach(function(result) {
		var row = result.item;
		var tr = document.createElement('tr');
        tr.innerHTML = '<td>' + row.title + '</td>' +
                       '<td>' + row.description + '</td>' +
                       '<td>' + row.grade + '</td>' +
                       '<td>' + row.quality + '</td>' +
                       '<td>' + row.height + '</td>' +
                       '<td>' + row.notes + '</td>' +
                       '<td><a href="' + row.link + '">Link</a></td>';
		tbody.appendChild(tr);
	});
});

