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
    document.getElementById("filterModal").style.display = "flex";
}

// Close the modal
function closeFilterModal() {
    document.getElementById("filterModal").style.display = "none";
}

//APPLY FILTER-->GO
function applyFilters() {
    var filterMetadata = get_filter_metadata();  

    // Make an AJAX request to send the data to the backend using Fetch API
    fetch('/path/to/handle_filter_submission/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(filterMetadata),
    })
    .then(response => {
        if (!response.ok) {
            // Handle errors
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {//success reponse
        var successMessage = 'Adding result of ' + data.exam_type + ' batch: ' + data.batch_number + ', sem: ' + data.semester + ', faculty: ' + data.faculty;
        toastr.success(successMessage);
        console.log(successMessage);
        window.location.href = `/add_result.html?semester=${data.semester}&batch=${data.batch_number}&faculty=${data.faculty}&exam_type=${data.exam_type}`;

    })
    .catch(error => {
        console.error('Fetch error:', error);
        toastr.error('An error occurred. Please try again.');
        closeFilterModal() ;
    })
    .finally(() => {
        // Close the modal after sending the request
        closeFilterModal() ;
    });
}

// Function to open the course modal
function openCourseModal() {
     document.getElementById("courseModal").style.display = "flex";
}

// Function to close the course modal
function closeCourseModal() {
   document.getElementById("courseModal").style.display = "none";
}

//TO GET THE FILTER VALUES
function get_filter_metadata(){
    var faculty=document.getElementById('faculty').value;
    var semester=document.getElementById('semester').value;
    var examType=document.getElementById('type').value;
    var batchNumber=document.getElementById('batchNumber').value;

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
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Data submitted successfully:', data);
        showAlert('Data submitted successfully!', 'success');
        // Optionally, you can perform any additional actions after successful submission
    })
    .catch(error => {
        console.error('Error submitting data:', error);
        showAlert('Error submitting data. Please try again.', 'error');
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

function deleteFile() {
    // Reset the file input
    document.getElementById('fileInput').value = '';

    // Optional: You can also clear the table or perform any other necessary cleanup
    clearTable();

    // Show a Toastr notification indicating file deletion
    showAlert('File deleted successfully!', 'success');
}

// Function to clear the table
function clearTable() {
    var table = document.getElementById('spreadsheetData');

    // Remove existing rows except the header row (if any)
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }
}

// Function to show Toastr notification
function showAlert(message, type) {
    toastr.options = {
        closeButton: true,
        progressBar: true,
        positionClass: 'toast-top-right',
        timeOut: 3000,
    };

    toastr[type](message);
}

        





