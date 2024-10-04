function follow(url1,url2,ele,token){
    $.ajax({
    url: url1,
    type: "POST",
    data : {
        csrfmiddlewaretoken: token
    },
    success: (data) => {
        if($("#f"+ele).text().includes("unfollow")) {
        $("#f"+ele).text("follow");
        }
        else{
        $("#f"+ele).text("unfollow");
        }

        $.ajax({
            url: url2,
            type: "GET",
            success: (data) => {
                text = $("#fc"+ele).text().split(" ")
                text[0]=data
                $("#fc"+ele).text(text.join(" "));
            },
            error: (error) => {
            console.log(error);
            }
            });    
    },
    error: (error) => {
    console.log(error);
    }
    });
};