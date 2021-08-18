// Call the dataTables jQuery plugin
$(document).ready(function() {
  var wop = $('#dataTable').DataTable({
    dom: "<'row'<'col-3'fi><'col-6 text-center'B><'col-3 text-center'p> >" +
    "<'row'<'col-12'tr>>" +
    "<'row'<'col-3'i><'col-6 text-center'B><'col-3 text-center'p> >",
    buttons: [
      {extend: "copy", className: "btn-dark"},
      {extend: "excel", className: "btn-dark"},
      {extend: "csv", className: "btn-dark"},
      {extend: "pdf", className: "btn-dark"},
      {extend: "print", className: "btn-dark"}
    ],
  });
});
