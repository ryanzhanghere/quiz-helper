//http://jsfiddle.net/E42XA/
$(document).ready(
    function () {
        //disable submission if no file is chosen
        $('input:file').change(
            function () {
                if ($(this).val()) {
                    $('button:submit').attr('disabled', false);

                }
            }
        );
    });