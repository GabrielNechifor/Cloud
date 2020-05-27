$(document).ready(function(){

    axios.get('https://cloud-test-shell.wl.r.appspot.com/saved_resources').then(response => {
        data = response["data"]
        var strdata = ""
          for (var i = 0; i < data.length; i++) {
            strdata += "<tr><td><a class='text-body' href='saved_resource_page?name="+data[i]["Name"]+"'>"+data[i]["Name"]+"</a></td><td>"+data[i]["Description"]+"</td><td>"+data[i]["Type"]+"</td><td>"+
                        data[i]["CreationDate"]+'</td><td><button id=btn'+i+' type="button" class="btn btn-primary">Delete</button></td></tr>'
            }
            strdata += "<tr><td></td><td></td><td></td><td></td><td></td></tr>"
            document.getElementById('row').innerHTML = strdata

            $("#show").click(function(){
                window.location.reload()
                /*
                var strdata = ""
                for (var i = 0; i < data.length; i++) {
                    strdata += "<tr><td>"+data[i]["Name"]+"</td><td>"+data[i]["Description"]+"</td><td>"+data[i]["Type"]+"</td><td>"+
                                data[i]["CreationDate"]+'</td><td><button id=btn'+i+' type="button" class="btn btn-primary">Delete</button></td></tr>'
                    }
                    strdata += "<tr><td></td><td></td><td></td><td></td><td></td></tr>"
                    document.getElementById('row').innerHTML = strdata

                    for (var i = 0; i < data.length; i++) {
                        var tmp_name = data[i]["Name"]
                        $("#btn"+i).click(function(){
                            axios.post('https://cloud-test-shell.wl.r.appspot.com/delete_resource', {name: tmp_name}).then(response => {
                                document.getElementById('row').innerHTML = response["data"]
                            });
                            
                        });
                    }
                    */
                    
            });

            $("#search").click(function(){
                var searchInput = document.getElementById('searchInput').value
                var strdata = ""
                for (var i = 0; i < data.length; i++) {
                    if (data[i]["Name"].search(searchInput) != -1 || data[i]["Description"].search(searchInput) != -1 
                        || data[i]["Type"].search(searchInput) != -1 ||
                        JSON.stringify(data[i]["CreationDate"]).search(searchInput) != -1){
                        strdata += "<tr><td><a class='text-body' href='saved_resource_page?name="+data[i]["Name"]+"'>"+data[i]["Name"]+"</a></td><td>"+data[i]["Description"]+"</td><td>"+data[i]["Type"]+"</td><td>"+
                                    data[i]["CreationDate"]+'</td><td><button id=btn'+i+' type="button" class="btn btn-primary">Delete</button></td></tr>'
                    }           
                  }
                  strdata += "<tr><td></td><td></td><td></td><td></td><td></td></tr>"
                  document.getElementById('row').innerHTML = strdata

                  for (var i = 0; i < data.length; i++) {
                    var tmp_name = data[i]["Name"]
                    $("#btn"+i).click(function(){
                        axios.post('https://cloud-test-shell.wl.r.appspot.com/delete_resource', {name: tmp_name}).then(response => {
                            document.getElementById('row').innerHTML = response["data"]
                        });
                    });
                }
                
            });   

            for (var i = 0; i < data.length; i++) {
                var tmp_name = data[i]["Name"]
                $("#btn"+i).click(function(){
                    axios.post('https://cloud-test-shell.wl.r.appspot.com/delete_resource', {name: tmp_name}).then(response => {
                        document.getElementById('row').innerHTML = response["data"]
                    });
                });
            }
            
        
    });       
});