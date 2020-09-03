document.addEventListener("DOMContentLoaded", ()=> {
    document.querySelector("#submit").disabled = true;

    document.querySelector("#text-field").onkeyup = () => {
        if(document.querySelector("#text-field").value.length > 0)
            document.querySelector("#submit").disabled = false;
        else
            document.querySelector("#submit").disabled = true;
    };

    document.querySelector("#message").onsubmit = ()=>{

        // Creating New Paragraph For Each New Message
        const para = document.createElement('div');
        const para2 = document.createElement('div'); 

        // Defining User Chat Pargraphs Styling And Behaviour
        para.style.textAlign= "center";
        para.style.maxWidth ="200px";
        para.style.overflowWrap = "anywhere";                                        
        para.style.padding = "3px";        
        para.style.position = "relative";
        para.style.float = "right";
        para.style.marginBottom = "5px";
        para.style.marginLeft = "200px";
        para.style.marginRight = "8px";
        para.style.marginTop = "12px";
        para.style.backgroundColor = "#007bff";  
        para.style.color = "#fff";              
        para.style.borderRadius = "7px";
        para.style.display = "inline" ;             
        
        // Defining Bot Chat Pargraphs Styling And Behaviour
        para2.style.textAlign= "center";
        para2.style.maxWidth ="200px";
        para.style.overflowWrap = "anywhere";                    
        para2.style.padding = "3px";        
        para2.style.position = "relative";
        para2.style.float = "left";
        para2.style.marginBottom = "5px";
        para2.style.marginRight = "200px";
        para2.style.marginLeft = "8px";
        para2.style.marginTop = "12px";
        para2.style.backgroundColor = "#efefef"; 
        para2.style.color = "#646464";
        para2.style.borderRadius = "7px";
        para2.style.display = "inline" ;
        


        const request = new XMLHttpRequest();
        const message = document.querySelector('#text-field').value;
        request.open('POST','/chat');
        request.onload = ()=>{
            const data = JSON.parse(request.responseText);
            para.innerHTML = document.querySelector("#text-field").value;
            para2.innerHTML = data.bot;
            
            document.querySelector(".container > #chat-area").append(para);
            chatWindow = document.getElementById('chat-area'); 
            var xH = chatWindow.scrollHeight;
            chatWindow.scrollTo(0, xH);
            setTimeout(()=> {document.querySelector(".container > #chat-area").append(para2);
            chatWindow = document.getElementById('chat-area'); 
            var xH = chatWindow.scrollHeight; 
            chatWindow.scrollTo(0, xH);},1000);
            

            // Auto Scroll To Bottom
        
        
        // Clearing Out The Text Field
        document.querySelector("#text-field").value = '';
        document.querySelector("#submit").disabled = true;
        };    
        
        const d = new FormData();
        d.append('message',message);

        request.send(d);             
        

        return false;
    };
});