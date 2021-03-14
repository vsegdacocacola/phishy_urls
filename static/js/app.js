n = 0

function render(title, data) {
    n++
    $("#accordionEx").prepend("<div class=\"card\"><div class=\"card-header\" role=\"tab\" id=\"headingOne-"+n+"\"><a data-toggle=\"collapse\" data-parent=\"#accordionEx\" href=\"#collapseOne-"+n+"\" aria-expanded=\"true\" aria-controls=\"collapseOne-"+n+"\"><h5 class=\"mb-0\">"+n+"-"+title+"</h5></a></div><div id=\"collapseOne-"+n+"\" class=\"collapse show\" role=\"tabpanel\" aria-labelledby=\"headingOne-"+n+"\" data-parent=\"#accordionEx\"><div class=\"card-body\" id=\"result-"+n+"\"></div></div></div>")
    if(data["image"]) {
        $("#result-"+n).append("<div class=\"screenshot\"><img src=\"data:image/png;base64, "+data["image"]+"\" class=\"rounded img-fluid\"></div>")
        delete data["image"]
    }
    $("#result-"+n).jsonView(data)
}
server_api = "http://127.0.0.1:5000/api"

function post_rest(method, params, callback) {
    api_url = server_api + '/' + method
    fetch(api_url, {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then (data => {
        render(method +" : " + JSON.stringify(params), data)
    })
    .catch((error) => {
        render(method +" : " + JSON.stringify(params), error)
    });
}

$("button#lookup").click(function() {
    url = $("input#url").val()
    hostname = new URL($("input#url").val()).hostname
    post_rest("dns",{ "host":hostname })
    post_rest("whois",{ "host":hostname })
    post_rest("url", {url: url})
    post_rest("head", {url: url} )
    post_rest("screenshot", {url: url, device: "mobile"})
    post_rest("screenshot", {url: url})
})

$(document).ready(function() {

});