let recognition;
const URL="http://127.0.0.1:8000";

loadFiles();

async function uploadFile(){

    let file=document.getElementById("file").files[0];

    if(!file){

        alert("Choose a file");

        return;

    }

    let formData=new FormData();

    formData.append("file",file);

    let response=await fetch(URL+"/upload",{

        method:"POST",

        body:formData

    });

    let data=await response.json();

    alert(data.message);

    loadFiles();

}

async function loadFiles(){

    let response=await fetch(URL+"/files");

    let data=await response.json();

    let filesDiv=document.getElementById("files");

    let dropdown=document.getElementById("filename");

    filesDiv.innerHTML="";

    dropdown.innerHTML="";

    data.files.forEach(file=>{

        filesDiv.innerHTML+=`

        <p>

            📄 ${file}

            <button onclick="deleteFile('${file}')">

                Delete

            </button>

        </p>

        `;

        dropdown.innerHTML+=`

        <option>

            ${file}

        </option>

        `;

    });

}

async function askQuestion(){

    let question=document.getElementById("question").value;

    let filename=document.getElementById("filename").value;

    let formData=new FormData();

    formData.append("question",question);

    formData.append("filename",filename);

    document.getElementById("loading").style.display="block";

    let response=await fetch(URL+"/ask",{

        method:"POST",

        body:formData

    });

    let data=await response.json();

    document.getElementById("loading").style.display="none";
    speak(data.answer);

    let chat=document.getElementById("chatBox");
    chat.innerHTML+=`
        <div class="user">
        <b> you:</b>${question}
         </div>
         <div class="bot">
        <b>DEEKSHITHA AI   </b>${data.answer}
        </div>`
;
document.getElementById("question").value="";
chat.scrollTop=chat.scrollHeight;
}

async function deleteFile(filename){

    await fetch(

        URL+"/delete?filename="+filename,

        {

            method:"DELETE"

        }

    );

    loadFiles();

}
async function startListening()
{
  if(!('webkitSpeechRecognition' in window))
  {
    alert("speech Recognition is not supported in this browser");
    return;
  }
  recognition =new webkitSpeechRecognition();
  recognition.lang="en-US";
  recognition.continuous=false;
  recognition.interimResults=false;
  recognition.start();
  recognition.onresult=function(event)
  {
    let speech=event.results[0][0].transcript;
    document.getElementById("question").value=speech;
    askQuestion();
  };
  recognition.onerror=function(event)
  {
    alert("speeech error"+event.error);
  };
}
function speak(text){
    window.speechSynthesis.cancel();
    let speech=new SpeechSynthesisUtterance(text);
    speech.lang="en-US";
    speech.pitch=1;
    speech.rate=1;
    speech.volume=1;
    speech.onend=function()
    {
        startListening();
    };
    window.speechSynthesis.speak(speech);
}