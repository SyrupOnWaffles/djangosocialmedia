function like(url1,url2,ele,token){
    $.ajax({
    url: url1,
    type: "POST",
    data : {
        csrfmiddlewaretoken: token
    },
    success: (data) => {
        if($("#r"+ele).text().includes("♡")) {
            $("#r"+ele).text("♥");
        }
        else{
            $("#r"+ele).text("♡");
        }

        $.ajax({
            url: url2,
            type: "GET",
            success: (data) => {
                text = $("#rl"+ele).text().split(" ")
                text[0]=data
                $("#rl"+ele).text(text.join(" "));
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