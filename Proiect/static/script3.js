$(document).ready(function(){
    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString)
    const tmp_name = urlParams.get('name')
    axios.post('https://cloud-test-shell.wl.r.appspot.com/saved_resource_page', {name: tmp_name}).then(response => {
    });
});