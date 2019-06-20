

var response;
var data;
var story_id;
var template = "";




function getStory()
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET",  "http://localhost:8080/api/story", false ); // false for synchronous request
    xmlHttp.send();
    response = JSON.parse(xmlHttp.responseText);
}
function getNextStory()
{
    var xmlHttp = new XMLHttpRequest();
    url = "http://localhost:8080/api/story?next_cursor=" + response.next_cursor 
    xmlHttp.open( "GET", url , false ); // false for synchronous request
    xmlHttp.send();
    response = JSON.parse(xmlHttp.responseText);
    displayStory();
}
function getNextComment(next_cursor, story_id)
{
    var xmlHttp = new XMLHttpRequest();
    story_id = story_id.substring(0, story_id.length - 1)
    console.log(story_id)
    url = "http://localhost:8080/api/comment?next_cursor=" + next_cursor + "&story_id=" + story_id;
    xmlHttp.open( "GET", url , false ); // false for synchronous request
    xmlHttp.send();
    response = JSON.parse(xmlHttp.responseText);
    console.log(response)
    displayNextComment(story_id, response)

}

function parseDay(date, _date) {
    if (date == 0) {
        return "Today " + _date;
    }
    else if (date == 1){
        return "Yesterday " + _date;
    }
    return _date;
}

function displayComment(comments, story_id, user_name) {
    var template = "";
    comments.comment.forEach(function (comment) {
        template += `<li class="list-group-item" > <span class="badge badge-secondary">` + comment.name +`</span>    ` + comment.comment +`</li>`;
    });
    if (comments.more){
        template += `<div id="` + comments.next_cursor + `">
                        <button onclick="getNextComment(this.parentNode.id, this.id)" id=` + story_id  + `y` + `>load more comment......</button>
                        </div>`;
    }
    return template;
}
function displayNextComment(story_id, response) {
    var el = document.getElementById(story_id + 'x')
    var temp = ""
    console.log(response)
    response.message.forEach(function (comment) {
        temp += `<li class="list-group-item" > <span class="badge badge-secondary">` + comment.name +`</span>    ` + comment.comment +`</li>`;
        
    });
    if (response.more){
        document.getElementById(story_id + "y" ).remove();
        temp += ` <div id="` + response.next_cursor + `">
        <button onclick="getNextComment(this.parentNode.id, this.id)" id=` + story_id  + `y` + `>load more comment......</button>
        </div>`;
        
    }
    else{
        document.getElementById(story_id + "y" ).remove();

    }
    el.innerHTML += temp
    console.log(temp)
    
}

function displayStory() {
    var stories = response.message;
    stories.forEach(function (story) {
        var oneDay = 24*60*60*1000;
        var date = new Date(story.time);
        date = new Date(date.getTime() + (330 + date.getTimezoneOffset() * 60000 ));
        var today =new Date();
        today =new Date(today.getTime() + (330 + today.getTimezoneOffset() * 60000 ));
        var diffDays = Math.round(Math.abs((today.getTime() - date.getTime())/(oneDay)));
        var day = parseDay(diffDays, date);
        
        template += `<div class="card w-75" >
                        <div class="card-body">
                            <h5 class="card-title">`+ story.name +`</h5>
                            <p  class="card-text">` + story.story +` </p>
                                <p  class="card-text"><small id="time" class="text-muted">` + day + `</small></p>
                                <div class="input-group mb-3">
                                    <input type="text" id="comment_content` + story.story_id + `" class="form-control" placeholder="Type your comment..." aria-label="Type your comment..." aria-describedby="button-addon2">
                                        <div class="input-group-append" id="` + story.story_id + `">
                                            <button onclick="postComment(this.parentNode.id)" class="btn btn-outline-info" type="button" id="button-addon2">Comment</button>
                                        </div>
                                    </div>
                                <ul class="list-group list-group-flush" id=` + story.story_id + 'x' + `>`
                                     + displayComment(story.comments, story.story_id, story.name) +
                                `</ul>
                            </div>
                        </div>`;
            });

            if (response.more){
                var loadMore = `<button onclick="getNextStory()">load more stories......</button>`;
                document.getElementById("more").innerHTML = loadMore;
            }
            else{
                document.getElementById("more").innerHTML = "";
            }

            document.getElementById("main").innerHTML = template;
}


function postStory() {
    var xmlHttp = new XMLHttpRequest();
    data = getUserDetails();
    xmlHttp.open( "POST",  "http://localhost:8080/api/story", false ); // false for synchronous request
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"name": data.name, "story": document.getElementById("story_content").value, "user_name": data.user_name});
    xmlHttp.send(data);
    getStory();
    document.getElementById("story_content").value = "";
}

function postComment(story_id) {
    
    var xmlHttp = new XMLHttpRequest();
    data = getUserDetails();
    xmlHttp.open( "POST",  "http://localhost:8080/api/comment", false ); // false for synchronous request
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"name": data.name, "comment": document.getElementById("comment_content" + story_id).value, "user_name": data.user_name, "story_id": story_id});
    xmlHttp.send(data);

    document.getElementById("comment_content" + story_id).value = "";
    displayStory();
}

getStory();
displayStory();
