const aside = document.getElementsByClassName("aside")[0];
const main = document.getElementsByClassName("main")[0];
const navbarHeight = document.getElementsByClassName("navbar")[0].clientHeight;
const windowHeight = window.innerHeight;
const profileOptions = document.getElementsByClassName("profileOptions")[0];

function adjustHeight(){
    aside.style.height = (windowHeight - navbarHeight) + 'px';
    main.style.height = (windowHeight - navbarHeight) + 'px';
    main.style.maxHeight = (windowHeight - navbarHeight) + 'px';

}
adjustHeight();

function showProfileOptions(){
    if (profileOptions.style.display === '' || profileOptions.style.display === 'none'){
        profileOptions.style.display = 'block';
    }
    else{
        profileOptions.style.display = 'none';
    }
}
 var box = document.getElementById('batta');
 var down = false;
 function togglenoti()
 {
    if(down){
       box.style.height = '0px';
       box.style.opacity = 0;
       down = false; 
    }
    else{
        box.style.opacity=1;
        down = true;
        box.style.height = '400px';
        // box.style.width = '220px';
    }
 }
function openFilterModal() {
    console.log('filter opened');
    document.getElementById("filterModal").style.display = "flex";
}

function closeFilterModal() {
    console.log('filter closed');
    document.getElementById("filterModal").style.display = "none";
}

function handleOptionClick(option) {
    openFilterModal();
    console.log('option click selected');
    let selectedOption = option;
    // Attach the selected option to the "Go" button
    document.getElementById('goButton').setAttribute('data-selected-option', selectedOption);
}
//GO button
function applyFilters() {
    console.log('go button');
    console.log('filter aplly garney thau, and we are firstly calling value liney funtion');
    var filterMetadata = get_filter_metadata();
    let selectedOption = document.getElementById('goButton').getAttribute('data-selected-option');
    console.log('aba fetch garna lagya');
    console.log('Filter Metadata:', filterMetadata);
    var url = document.querySelector('button[data-url]').dataset.url;
    console.log (url);
    var formData = new FormData();
    switch (selectedOption) {
        case 'add_result':
            Object.entries(filterMetadata).forEach(([key, value]) => {
                formData.append(key, value);
            });
        
            // Add CSRF token to the headers
            formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        
            fetch(url, {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                console.log('response lina aako yeta');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                var successMessage = 'Adding result of ' + data.data.exam_type + ' batch: ' + data.data.batch_number + ', sem: ' + data.data.semester + ', faculty: ' + data.data.faculty;
                console.log(successMessage);
                window.location.href =`/examsection/addresult/${data.data.semester}/${data.data.batch_number}/${data.data.faculty}/${data.data.exam_type}/`;
            })
            .catch(error => {
                console.log('error catch garyo');
                console.error('Fetch error:', error);
                closeFilterModal();
            })
            .finally(() => {
                console.log('regardless of k k vayo, we are onto closing filter now');
                closeFilterModal();
            });
            break;
            case 'view_result':
                break;
            case 'student_analysis':
                break;
    }
}
//COOKIESSSS
function getCookie(name) {
    console.log('cookies lina aako');
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            console.log('cookies ko loop');
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log('sakkyo cookies liney');
    if (cookieValue === null) {
        console.error('Cookie with name ' + name + ' not found. Cookies may be disabled.');
    }
    return cookieValue;
}

function openCourseModal() {
     document.getElementById("courseModal").style.display = "flex";
}

function closeCourseModal() {
   document.getElementById("courseModal").style.display = "none";
}

function get_filter_metadata(){
    var faculty=document.getElementById('faculty').value;
    var semester=document.getElementById('semester').value;
    var examType=document.getElementById('type').value;
    var batchNumber=document.getElementById('batchNumber').value;
    console.log('hamle id bata liyou hai filter haru ko value and tala yeslai return garya xa');
    console.log(faculty, semester, examType, batchNumber);
    return {
        faculty:faculty,
        semester:semester,
        exam_type:examType,
        batch_number:batchNumber
    };
}
function importData() {
    var fileInput = document.getElementById('fileInput');

    fileInput.addEventListener('change', function (e) {
        var file = e.target.files[0];

        var reader = new FileReader();

        reader.onload = function (e) {
            var data = e.target.result;
            var workbook = XLSX.read(data, { type: 'binary' });
            var sheet = workbook.Sheets[workbook.SheetNames[0]];
            var jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

            // Display data in the existing table
            displayData(jsonData);
        };

        reader.readAsBinaryString(file);
    });

    // Trigger click event on the file input to open the file selection dialog
    fileInput.click();
}

function displayData(data) {
    var table = document.getElementById('spreadsheetData');

    // Remove existing rows except the header row (if any)
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    // Add data rows
    for (var j = 1; j < data.length; j++) {
        var row = table.insertRow();
        for (var k = 0; k < data[j].length; k++) {
            var cell = row.insertCell();
            cell.textContent = data[j][k];
        }
    }
}
function submitData() {
    // You need to implement this function to send the data to your server for updating the database
    // This can be done using AJAX (e.g., Fetch API or XMLHttpRequest) to send the data to your server endpoint
    // The server-side code should handle the data and update the database accordingly
    // Example AJAX code (using Fetch API):
    fetch('/submit_data_endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: getDataFromTable() }), // Adjust this part based on your data structure
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data submitted successfully:', data);
        // Optionally, you can perform any additional actions after successful submission
    })
    .catch(error => {
        console.error('Error submitting data:', error);
        // Optionally, you can handle errors or display an error message
    });
}

// Helper function to get data from the table
function getDataFromTable() {
    // Implement this function to extract data from your table
    // You may need to loop through the table rows and cells to collect the data
    // Return the data in a suitable format (e.g., array of objects)
    // Example structure: [{ student_name: 'John', subject: 'Math', marks: 90 }, ...]
    // Adjust this based on your actual table structure
    return [];
}