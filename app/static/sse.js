//document.body.style.cursor = 'none';
var previous = []

window.onload=reset;
document.onclick=reset;
var source = new EventSource("/count");
source.onmessage = function(event) {
    var data = JSON.parse(event.data);
    for (var key in data) {
      if (data.hasOwnProperty(key)) {
        previous[key] += data[key];
        document.getElementById(key).innerHTML = previous[key];
      }
    }
}
function reset()
{
    for (var i = 0; i < 7; i++) {
        previous[i] = 0;
        document.getElementById(i).innerHTML = previous[i];
    }
}
