document.addEventListener('DOMContentLoaded', function()
{
   document.getElementById('Form').addEventListener('submit', function(event) {
       alert('Application submitted successfully');
   });
});


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('EditForm').addEventListener('submit', function(event) 
    {
      alert('job edited successfully');  
    });
});

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('mailform').addEventListener('submit', function(event) 
  {
    alert('Mail sent');  
  });
});