

var response;
var URL = "http://localhost:8080/";
var PRODUCTION_URL = "https://full-services.appspot.com/"
var data;
var story_id;
var template = "";




function getStory() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET",  URL + "api/story", false ); // false for synchronous request
    xmlHttp.send();
    response = JSON.parse(xmlHttp.responseText);
    displayStory()
}
function getNextStory()
{
    if (response.more){
    var xmlHttp = new XMLHttpRequest();
    url = URL + "api/story?next_cursor=" + response.next_cursor
    xmlHttp.open( "GET", url , false ); // false for synchronous request
    xmlHttp.send();
    response = JSON.parse(xmlHttp.responseText);
    displayStory();
    }
}
function getNextComment(next_cursor, story_id)
{
    var res
    var xmlHttp = new XMLHttpRequest();
    story_id = story_id.substring(0, story_id.length - 12)
    url = URL + "api/comment?next_cursor=" + next_cursor + "&story_id=" + story_id;
    xmlHttp.open( "GET", url , false ); // false for synchronous request
    xmlHttp.send();
    res = JSON.parse(xmlHttp.responseText);
    displayNextComment(story_id, res)

}
function updateLike(story_id) {
    story_id = story_id.substring(0, story_id.length - 4)
    var res
    data = getUserDetails()
    var xmlHttp = new XMLHttpRequest();
    url = URL + "api/like?user_name=" + data.user_name + "&story_id=" + story_id;
    xmlHttp.open( "GET", url , false ); // false for synchronous request
    xmlHttp.send();
    res = JSON.parse(xmlHttp.responseText);
    document.getElementById(story_id + 'like_count').innerHTML = `<div id="` + story_id + `like_count">` + res.count + `</div>`;
    document.getElementById(story_id + 'like_status').innerHTML = `<button onclick="updateLike(this.id)" class="btn btn-outline-` + likeStatus(res.status) +`" id="` + story_id + `like` + `">like</button>`;


}

function likeStatus(liked) {
    if (liked) {
        return "success"
    } else {
        return "danger"
    }

}

function parseDay(today, _date) {
    if (_date.getDate() == today.getDate()) {
        return "Today " + _date.toLocaleTimeString();
    }
    else if (_date.getDate() == today.getDate() - 1){
        return "Yesterday " + _date.toLocaleTimeString();
    }
    return _date.toLocaleString();
}

function displayComment(comments, story_id, user_name) {
    var template = "";
    comments.comment.forEach(function (comment) {
        template += `<li class="list-group-item" > <span class="badge badge-secondary">` + comment.name +`</span>    ` + comment.comment +`</li>`;
    });
    if (comments.more){
        template += `<div id="` + comments.next_cursor + `">
                        <a href="#" onclick="getNextComment(this.parentNode.id, this.id); return false;" id=` + story_id  + `more_comment` + `>load more comment......</a>
                        </div>`;
    }
    return template;
}
function displayNextComment(story_id, response) {
    var el = document.getElementById(story_id + 'comment')
    var temp = ""
    response.message.forEach(function (comment) {
        temp += `<li class="list-group-item" > <span class="badge badge-secondary">` + comment.name +`</span>    ` + comment.comment +`</li>`;
        
    });
    if (response.more){
        document.getElementById(story_id + "more_comment" ).remove();
        temp += ` <div id="` + response.next_cursor + `">
        <a href="#" onclick="getNextComment(this.parentNode.id, this.id); return false;" id=` + story_id  + `more_comment` + `>load more comment......</a>
        </div>`;
        
    }
    else{
        document.getElementById(story_id + "more_comment" ).remove();

    }
    el.innerHTML += temp
}

function displayStory() {
    var stories = response.message;
    stories.forEach(function (story) {
        var date = new Date(story.time);
        var today =new Date();
        var day = parseDay(today, date);
        template += `<div class="card w-75" >
                        <div class="card-body">
                            <h5 class="card-title">`+ story.name +`</h5>
                            <img src="http://storage.googleapis.com/full-services.appspot.com/story/`+ story.story_id+`.jpg" style="height: 15%; width: 30%">
                            <p  class="card-text">` + story.story +` </p>
                                <p  class="card-text"><small id="time" class="text-muted">` + day + `</small></p>

                                <div class="input-group mb-3">
                                    <input type="text" id="comment_content` + story.story_id + `" class="form-control" placeholder="Type your comment..." aria-label="Type your comment..." aria-describedby="button-addon2">
                                        <div class="input-group-append" id="` + story.story_id + `">
                                            <button onclick="postComment(this.parentNode.id)" class="btn btn-outline-info" type="button" id="button-addon2">Comment</button>
                                        </div>
                                    </div>
                                    <div id="` + story.story_id + `like_count">` + story.like_count + `</div>
                                    <div id="` + story.story_id + 'like_status' + `">
                                    <button onclick="updateLike(this.id)" class="btn btn-outline-` + likeStatus(story.liked) +`" id="` + story.story_id + `like` + `">like</button>
                                    </div>
                                <ul class="list-group list-group-flush" id=` + story.story_id + 'comment' + `>`
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




postStory = async () => {
    user = getUserDetails();
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"name": user.name, "story": document.getElementById("story_content").value, "user_name": user.user_name})
    };

    const data = await fetch(URL+"api/story", settings)
    .then(response => response.json())
    .then(json => {
        return json;
    })
    .catch(e => {
        return e
    });
    document.getElementById('story_content').value = "";
    document.getElementById("preview_image").innerHTML = `                                <img id="img" src="" class="imgResponsiveMax" style="height: 200px; width: 200px" alt="" />
    <button type="button" class="close Close" aria-label="Close" onclick="onClickMe()" >
        <span aria-hidden="true">&times;</span>
      </button>`;
    document.getElementById('preview_image').style.visibility = "hidden";
    template = "";
    var file = document.getElementById('fileInput').files[0];
    var xmlHttp = new XMLHttpRequest();
    url =data.message
    xmlHttp.open( "PUT", url , true ); // false for synchronous request
    xmlHttp.onload = () => {
        const status = xmlHttp.status;
        if (status === 200) {

        } else {
          alert("Something went wrong!");
        }
      };
      xmlHttp.onreadystatechange = function()
        {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            {
                getStory();// Another callback here
            }
        };
      
      xmlHttp.onerror = () => {
        alert("Something went wrong");
      };
      xmlHttp.setRequestHeader('Content-Type', file.type);
      xmlHttp.send(file);

    
    return data;
}



postComment = async (story_id) => {
    user = getUserDetails();
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"name": user.name, "comment": document.getElementById("comment_content" + story_id).value, "user_name": user.user_name, "story_id": story_id})
    };
    const data = await fetch(URL+"api/comment", settings)
    .then(response => response.json())
    .then(json => {
        return json;
    })
    .catch(e => {
        return e
    });
    document.getElementById("comment_content" + story_id).value = "";
    template = "";
    setTimeout(getStory,1000)
    return data


}

 function chooseFile(){

   document.getElementById("fileInput").click();
    
 }

function previewImage(){

      var file = document.getElementById('fileInput').files[0];
      var reader  = new FileReader();
      reader.onload = function(e)  {
          var image = document.getElementById("img");
          image.src = e.target.result;
       }
       reader.readAsDataURL(file);
   document.getElementById('preview_image').style.visibility = "visible";

}

function onClickMe(){
    document.getElementById("preview_image").innerHTML = `                                <img id="img" src="" class="imgResponsiveMax" style="height: 200px; width: 200px" alt="" />
    <button type="button" class="close Close" aria-label="Close" onclick="onClickMe()" >
        <span aria-hidden="true">&times;</span>
      </button>`;
    document.getElementById('fileInput').value = "";
    document.getElementById('preview_image').style.visibility = "hidden";
}


getStory();


var whenScrlBottom = function() {

    var win_h = (self.innerHeight) ? self.innerHeight : document.body.clientHeight;    
    var scrl_pos = window.pageYOffset ? window.pageYOffset : document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop;
    if (document.body.scrollHeight <= (scrl_pos + win_h)) {
        setTimeout(getNextStory,1000)
    }
  }
  
  window.onscroll = whenScrlBottom;