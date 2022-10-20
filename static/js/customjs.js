
  $("#id_bank").change(function () {
      const bankID = $(this).val();  // get the selected  ID from the HTML dropdown list 
      $.ajax({                       // initialize an AJAX request
          type: "POST",
          url: '{% url "load-bank-branches" %}',
          data: {
              'bank_id': bankID,       // add the  id to the POST parameters
              'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
          },
          success: function (data) {   // `data` is from `load-bank-branches` view function
              let html_data = '<option value="">Choose a bank branch</option>';
              data.forEach(function (data) {
                  html_data += `<option value="${data.id}">${data.name}</option>`
              });
              $("#id_branch").html(html_data); // replace the contents  with the data that came from the server
          }
      });
  });
