

var msg;
var data;
var story_id;



function getStory()
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET",  "http://localhost:8080/api/story", false ); // false for synchronous request
    xmlHttp.send();
    msg = JSON.parse(xmlHttp.responseText);
    displayStory()
}
function parseDay(date, _date) {
    if (date == 0) {
        return "Today " + _date
    }
    else if (date == 1){
        return "Yesterday " + _date
    }
    return date
}

function displayComment(comments) {
    var template = ""
    comments.forEach(function (comment) {
        template += `<li class="list-group-item"> <span class="badge badge-secondary">` + comment.name +`</span>    ` + comment.comment +`</li>`
    });
    return template
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
        var day = parseDay(diffDays, date)
        
        story_id = story.story_id

        
        template += `<div class="card w-75" >
                        <div class="card-body">
                            <h5 class="card-title">`+ story.name +`</h5>
                            <p  class="card-text">` + story.story +` </p>
                                <p  class="card-text"><small id="time" class="text-muted">` + day + `</small></p>
                                <div class="input-group mb-3">
                                    <input type="text" id="comment_content" class="form-control" placeholder="Type your comment..." aria-label="Type your comment..." aria-describedby="button-addon2">
                                        <div class="input-group-append" id="` + story.story_id + `">
                                            <button onclick="postComment(this.parentNode.id)" class="btn btn-outline-info" type="button" id="button-addon2">Comment</button>
                                        </div>
                                    </div>
                                <ul class="list-group list-group-flush">`
                                     + displayComment(story.comments) +
                                `</ul>
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

function postComment(story_id) {
    
    var xmlHttp = new XMLHttpRequest();
    data = getUserDetails()
    xmlHttp.open( "POST",  "http://localhost:8080/api/comment", false ); // false for synchronous request
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"name": data.name, "comment": document.getElementById("comment_content").value, "user_name": data.user_name, "story_id": story_id});
    xmlHttp.send(data);
    getStory();
    document.getElementById("story_content").value = ""
}

getStory();
