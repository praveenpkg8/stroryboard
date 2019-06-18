

var msg;
var data;



function getStory()
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET",  "http://localhost:8080/api/story", false ); // false for synchronous request
    xmlHttp.send();
    msg = JSON.parse(xmlHttp.responseText);
    displayStory()
}
function parseDay(date) {
    if (date == 0) {
        return "Today"
    }
    else if (date == 1){
        return "Yesterday"
    }
    return date
}

function displayStory() {
    var stories = msg.message
    var template = ""
    stories.forEach(function (story) {
        var oneDay = 24*60*60*1000;
        var date = new Date(story.time);
        date = new Date(date.getTime() + (330 + date.getTimezoneOffset() * 60000 ));
        var today =new Date();
        today =new Date(today.getTime() + (330 + today.getTimezoneOffset() * 60000 ));
        var diffDays = Math.round(Math.abs((today.getTime() - date.getTime())/(oneDay)));
        var day = parseDay(diffDays)
        template += `<div class="card w-75" >
        <div class="card-body">
          <h5 class="card-title">`+ story.name +`</h5>
          <p  class="card-text">` + story.story +` </p>
            <p  class="card-text"><small id="time" class="text-muted">` + day + `</small></p>
        </div>
        </div>`;
            });
            document.getElementById("main").innerHTML = template;
}

function postStory() {
    var xmlHttp = new XMLHttpRequest();
    data = getUserDetails()
    xmlHttp.open( "POST",  "http://localhost:8080/api/story", false ); // false for synchronous request
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"name": data.name, "story": document.getElementById("story_content").value, "user_name": data.user_name});
    xmlHttp.send(data);
    getStory();
    document.getElementById("story_content").value = ""
}

getStory();
