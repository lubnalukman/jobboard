document.addEventListener("DOMContentLoaded", function() 
{
    const mobileMenu = document.getElementById('mobile-menu');
    const nav = document.querySelector('.navbar-nav');

    mobileMenu.addEventListener('click', function() {
        nav.classList.toggle('nav-active');
    });
});

function deleteJob(event, jobId) {
    event.preventDefault();
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/joblist/delete/${jobId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ id: jobId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById(`job-${jobId}`).remove();
            alert(data.message);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was an error deleting the job.");
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('Form').addEventListener('submit', function(event) {
        alert('Profile updated successfully');
    });
});