const API_URL="http://127.0.0.1:8000";
const uploadBtn=document.getElementById("uploadBtn");
const sendBtn=document.getElementById("sendBtn");
const voiceBtn=document.getElementById("voiceBtn");
const deleteBtn=document.getElementById("deleteBtn");
const clearBtn=document.getElementById("clearChat");
const pdfFile=document.getElementById("pdfFile");
const uploadStatus=document.getElementById("uploadStatus");
const question=document.getElementById("question");
const chatBox=document.getElementById("chatBox");
const typing=document.getElementById("typing");
const fileList=document.getElementById("fileList");
let uploadedFiles=[];
let currentFile="";
function scrollBottom(){
chatBox.scrollTop=chatBox.scrollHeight;
}
function showTyping(){
typing.style.display="flex";
scrollBottom();
}
function hideTyping(){
typing.style.display="none";
}
function addUserMessage(text){
const div=document.createElement("div");
div.className="user-message";
div.innerHTML=`
<div class="message">${text}</div>
<div class="avatar">👤</div>
`;
chatBox.appendChild(div);
scrollBottom();
}

function addBotMessage(text){
const div=document.createElement("div");
div.className="bot-message";
div.innerHTML=`
<div class="avatar">🤖</div>
<div class="message">${text}</div>
`;
chatBox.appendChild(div);
scrollBottom();
}
function refreshFiles(){
fileList.innerHTML="";
if(uploadedFiles.length===0){
fileList.innerHTML="<p>No file uploaded</p>";
return;
}
uploadedFiles.forEach(file=>{
const div=document.createElement("div");
div.className="file-card";
div.innerHTML=`
<input type="checkbox" class="file-check" value="${file}" checked>
<span>${file}</span>
<button class="delete-file" data-file="${file}">🗑</button>
`;
fileList.appendChild(div);
});
}
uploadBtn.addEventListener("click",async()=>{
if(pdfFile.files.length===0){
alert("Please choose a PDF.");
return;
}
const formData=new FormData();
formData.append("file",pdfFile.files[0]);
uploadStatus.innerHTML="Uploading...";
try{
const response=await fetch(API_URL+"/upload",{
method:"POST",
body:formData
});
const data=await response.json();
uploadStatus.innerHTML="✅ Upload Successful";
currentFile=data.filename;
uploadedFiles.push(currentFile);
refreshFiles();
addBotMessage("Document uploaded successfully. You can now ask questions.");
}
catch(error){
console.log(error);
uploadStatus.innerHTML="❌ Upload Failed";
}
});
sendBtn.addEventListener("click",askQuestion);
question.addEventListener("keypress",function(e){
if(e.key==="Enter"&&!e.shiftKey){
e.preventDefault();
askQuestion();
}
});


async function askQuestion(){
const q=question.value.trim();
if(q===""){
alert("Please enter a question.");
return;
}
if(currentFile==="")
{
    alert("please upload a pdf first");
    return;
}
addUserMessage(q);
question.value="";
showTyping();
const formData=new FormData();
formData.append("question",q);
const selected=document.querySelector(".file-check:checked");

if(!selected){
alert("Please select a document.");
hideTyping();
return;
}

formData.append("filename",selected.value);

try{
const response=await fetch(API_URL+"/ask",{
method:"POST",
body:formData

});
const data=await response.json();
hideTyping();
addBotMessage(data.answer);
speak(data.answer);
}catch(error)
{
    hideTyping();
    console.log(error);
    addBotMessage("server Error");
}
}

function speak(text){
if(!("speechSynthesis" in window)){
return;
}
window.speechSynthesis.cancel();
const speech=new SpeechSynthesisUtterance();
speech.text=text;
speech.rate=1;
speech.pitch=1;
speech.volume=1;
const voices=window.speechSynthesis.getVoices();
if(voices.length>0){
speech.voice=voices.find(v=>v.lang.includes("en"))||voices[0];
}
window.speechSynthesis.speak(speech);
}
window.speechSynthesis.onvoiceschanged=function(){
window.speechSynthesis.getVoices();
};
voiceBtn.addEventListener("click",()=>{
if(!('webkitSpeechRecognition'in window)){
alert("Speech Recognition is not supported in this browser.");
return;
}
const recognition=new webkitSpeechRecognition();
recognition.lang="en-US";
recognition.interimResults=false;
recognition.maxAlternatives=1;
voiceBtn.innerHTML="🎤 Listening...";
recognition.start();
recognition.onresult=function(event){
const transcript=event.results[0][0].transcript;
question.value=transcript;
voiceBtn.innerHTML="🎤 Voice";
};
recognition.onerror=function(){
voiceBtn.innerHTML="🎤 Voice";
};
recognition.onend=function(){
voiceBtn.innerHTML="🎤 Voice";
};
});

clearBtn.addEventListener("click",()=>{
if(!confirm("Clear chat history?"))return;
chatBox.innerHTML=`
<div class="bot-message">
<div class="avatar">🤖</div>
<div class="message">
Hello 👋<br><br>
I'm <b>DEEKSHITHA AI</b>.<br><br>
Upload your PDF and ask me anything.
</div>
</div>
`;
chatBox.appendChild(typing);
scrollBottom();
});

deleteBtn.addEventListener("click",async()=>{

if(uploadedFiles.length===0){
alert("No files to delete.");
return;
}

if(!confirm("Delete all uploaded documents?")) return;

for(const file of uploadedFiles){

await fetch(API_URL+"/delete?filename="+encodeURIComponent(file),{
method:"DELETE"
});

}

uploadedFiles=[];
currentFile="";
refreshFiles();

uploadStatus.innerHTML="";
pdfFile.value="";

addBotMessage("✅ All documents deleted successfully.");

});
window.onload=async()=>{
scrollBottom();
question.focus();
try{
    const response =await fetch(API_URL+"/files");
    const data=await response.json();
    uploadedFiles=data.files;
    refreshFiles();
    if(uploadedFiles.length>0)
    {
        currentFile=uploadedFiles[0];
    }
}catch(error){
    console.log(error);
}
};
setInterval(()=>{
const dot=document.querySelector(".online-dot");
if(dot){
dot.style.opacity=dot.style.opacity==="0.4"?"1":"0.4";
}
},800);
document.addEventListener("dragover",(e)=>{
e.preventDefault();
});
document.addEventListener("drop",(e)=>{
e.preventDefault();
if(e.dataTransfer.files.length>0){
pdfFile.files=e.dataTransfer.files;
uploadStatus.innerHTML="File ready for upload.";
}
});
question.addEventListener("input",()=>{
question.style.height="auto";
question.style.height=question.scrollHeight+"px";
});
document.addEventListener("keydown",(e)=>{
if(e.ctrlKey&&e.key==="Enter"){
askQuestion();
}
});

document.addEventListener("click",async(e)=>{
if(e.target.classList.contains("delete-file")){
const filename=e.target.dataset.file;
await fetch(API_URL+"/delete?filename="+encodeURIComponent(filename),{
method:"DELETE"
});
uploadedFiles=uploadedFiles.filter(f=>f!==filename);
if(currentFile===filename){
currentFile="";
}
refreshFiles();
}
});
const emailMenuBtn=document.getElementById("emailMenuBtn");
const emailSection=document.getElementById("emailSection");
const chatSection=document.getElementById("chatSection");
const backToChat=document.getElementById("backToChat");
const generateEmail=document.getElementById("generateEmail");

emailMenuBtn.addEventListener("click",()=>{
chatSection.style.display="none";
emailSection.style.display="block";
});

backToChat.addEventListener("click",()=>{
emailSection.style.display="none";
chatSection.style.display="block";
});

generateEmail.addEventListener("click",async()=>{

const receiver=document.getElementById("receiver").value.trim();
const prompt=document.getElementById("emailPrompt").value.trim();

if(receiver===""||prompt===""){
alert("Please fill all fields.");
return;
}

const formData=new FormData();
formData.append("receiver",receiver);
formData.append("prompt",prompt);

try{

const response=await fetch(API_URL+"/send-email-ai",{
method:"POST",
body:formData
});

const data=await response.json();

if(response.ok){
alert("✅ Email sent successfully.");
document.getElementById("receiver").value="";
document.getElementById("emailPrompt").value="";
}else{
alert(data.detail||"Unable to send email.");
}

}catch(error){
console.log(error);
alert("Server Error");
}

});