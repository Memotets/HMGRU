// Call the dataTables jQuery plugin
$(document).ready(function() {
  var wop = $('#dataTable').DataTable({
    dom: "<'row'<'col-3'fi><'col-6 text-center'B><'col-3 text-center'p> >" +
    "<'row'<'col-12'tr>>" +
    "<'row'<'col-3'i><'col-6 text-center'B><'col-3 text-center'p> >",
    data: [],
    buttons: [
      {
        text: "Toggle", className:"btn-dark",
        action:function (IpEdificios, putNodes){
          let table = $('#dataTable').DataTable();
          var data = table.rows( function ( idx, data,node) {
              return $(node).find('input[type="checkbox"][class="checkToggle"]').prop('checked');
          } )
          .indexes()
          .toArray();
          let nodos=[];
          data.forEach( d => {
            nodos.push( putNodes[d]);
          })
          data = {
            "ip" : IpEdificios,
            "nodos" : nodos
          }
          console.log(data);

        }
      }, 

      {
        text: "Check all", className:"btn-dark",
        action: function (){
          let table = $('#dataTable').DataTable();

          table.cells(null, 5).every( function () {
            var cell = this.node();

            $(cell).find('input[type="checkbox"][class="checkToggle"]').prop('checked', true); 
          });

        }
      },
      {
        text: "Uncheck all", className:"btn-dark",
        action: function (){
          let table = $('#dataTable').DataTable();

          table.cells(null, 5).every( function () {
            var cell = this.node();

            $(cell).find('input[type="checkbox"][class="checkToggle"]').prop('checked', false); 
          });

        }
      },

    ],
  });
});
