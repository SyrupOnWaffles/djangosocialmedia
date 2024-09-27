function like(url1,url2,ele,token){
    console.log(url2)
    $.ajax({
    url: url1,
    type: "POST",
    data : {
        csrfmiddlewaretoken: token
    },
    success: (data) => {
        if($("#p"+ele).text().includes("♡")) {
            $("#p"+ele).text("♥");
        }
        else{
            $("#p"+ele).text("♡");
        }

        $.ajax({
            url: url2,
            type: "GET",
            success: (data) => {
                $("#pl"+ele).text(data+ " likes");
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