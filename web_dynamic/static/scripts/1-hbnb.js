$(document).ready(function () {
    $('input[type=checkbox]').change(function () {
      const nameList = [];
      const idAmenity = [];
      
      $('input[type=checkbox]:checked').each(function () {
        nameList.push($(this).attr('data-name'));
        idAmenity.push($(this).attr('data-id'));
      });
  
      if (nameList.length > 0) {
        $('.amenities h4').text(nameList.join(', '));
      } else {
        $('.amenities h4').html('&nbsp;');   
      }
  
      console.log(idAmenity);
    });
  });
