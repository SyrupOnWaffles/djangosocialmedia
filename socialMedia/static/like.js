function like(url,ele,token){
    console.log(url)
    $.ajax({
    url: url,
    type: "POST",
    data : {
        csrfmiddlewaretoken: token
    },
    success: (data) => {
        if($("#p"+ele).text().includes("♡")) {
            $("#p"+ele).text("♥");
            console.log("yeah")
        }
        else{
            $("#p"+ele).text("♡");
            console.log("no")
        }
    },
    error: (error) => {
    console.log(error);
    }
    });
};