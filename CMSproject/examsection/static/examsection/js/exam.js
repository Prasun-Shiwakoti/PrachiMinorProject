function showProfileOptions() {
    var profileOptions = document.querySelector('.userProfileContainer .profileOptions');

    // Toggle the visibility of profileOptions
    if (profileOptions.style.display === 'block') {
        profileOptions.style.display = 'none';
    } else {
        profileOptions.style.display = 'block';
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
//GO button
function applyFilters() {
    console.log('filter aplly garney thau, and we are firstly calling value liney funtion');
    var filterMetadata = get_filter_metadata();
    console.log('aba fetch garna lagya');
    console.log('Filter Metadata:', filterMetadata);
    var adminId = document.querySelector('[data-admin-id]').dataset.adminId;
    var url = document.querySelector('button[data-url]').dataset.url;
    var formData = new FormData();

    // Append each key-value pair to the FormData object
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
        window.location.href =`/examsection/addresult/${data.data.semester}/${data.data.batch_number}/${data.data.faculty}/${data.data.exam_type}/${adminId}`;
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

    fileInput.getElementById('fileInput').addEventListener('change', function (e) {
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
    // fetch('/submit_data_endpoint', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ data: getDataFromTable() }), // Adjust this part based on your data structure
    // })
    // .then(response => response.json())
    // .then(data => {
    //     console.log('Data submitted successfully:', data);
    //     // Optionally, you can perform any additional actions after successful submission
    // })
    // .catch(error => {
    //     console.error('Error submitting data:', error);
    //     // Optionally, you can handle errors or display an error message
    // });
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