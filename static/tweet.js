function Tweet(data) {
    this.Body = ko.observable(data.Body);
    this.Timestamp = ko.observable(data.Timestamp);
    this.username = ko.observable(data.Tweetby);
    this.id = ko.observable(data.id);
}

function TweetListViewModel() {
    var self = this;
    self.tweets_list = ko.observableArray([]);
    self.username = ko.observable();
    self.Body = ko.observable();
    //session_name = session['name'];
    //self.Timestamp = ko.observable();    
    //self.id = ko.observable();

    self.addTweet = function () {
        self.save();
        self.Body("");
    };

    $.getJSON('/api/v2/tweets', function (tweetModels) {
        var t = $.map(tweetModels.tweets_list, function(item) {
            return new Tweet(item);
        });
        self.tweets_list(t);
    });

    self.save = function () {
        return $.ajax({
            url: '/api/v2/tweets',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify({
                'username': self.username(),
                'Body': self.Body(),
            }),
            success: function (data) {
                alert("success")
                console.log("Pushing to users array 1");
                console.log(data);
                self.tweets_list.push(new Tweet(data)); 
                return;
            },
            error: function () {
                return console.log("Failed");
            }
        });
    };
}
ko.applyBindings(new TweetListViewModel());