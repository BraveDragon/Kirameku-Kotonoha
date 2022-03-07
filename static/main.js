const app = new Vue({
    el: "#app",
    data:{
      fullPoem:"",
      firstPoem:"",
      secondPoem:"",
      firstTop:"",
      secondTop:"",
      feeling:0,//デフォルトは0、ポジティブなら1、ネガティブなら-1
      result:{}
    },
    methods:{
        createPoem:function(){
            this.poem = "";
            const URL = "/poem";
            //先頭の2語が入力されている時のみ動作
            if(this.firstTop === "" || this.secondTop === ""){
                return;
            }
            //リクエストがあるまでは待機用の表示に切り替え
            Vue.set(app,"firstPoem","生成中...");
            Vue.set(app,"secondPoem","");
            axios.get(URL,{params:{
                firstTop:encodeURIComponent(this.firstTop),
                secondTop:encodeURIComponent(this.secondTop)}})
                .then(response => {
                    Vue.set(app,"firstPoem",response.data["firstPoem"]);
                    Vue.set(app,"secondPoem",response.data["secondPoem"]);                    
                    if (response.data["positiveFlag"] === true) {
                        Vue.set(this,"feeling",1);
                    }
                    else{
                        Vue.set(this,"feeling",-1);
                    }
                    createdEvent = new Event("createdPoem");
                    window.dispatchEvent(createdEvent);
                });
        },
        copyOnClipboard:function() {
            //詩ができている時のみ動作
            if(this.firstPoem === "" || this.secondPoem === ""){
                return;
            }
            return navigator.clipboard.writeText(this.firstPoem+"\n"+this.secondPoem);
            
        },
        goToTwitter:function() {
            open("https://twitter.com/home");
            
        }
    }

})

function setImage() {
    const element = document.getElementById("feelingImage");
    if(app.$data["feeling"] === 0){
        element.style.visibility = "hidden";
        return;
    }
    else if(app.$data["feeling"] === 1) {
        element.style.visibility = "visible";
        element.src = "static/109428.png"
    }else if(app.$data["feeling"] === -1){
        element.style.visibility = "visible";
        element.src = "static/sadFace.png"
    }
    
}

window.addEventListener("createdPoem",setImage);

let IntervalHandler = 0;
function setAnimation() {
    const field = document.querySelector("#animation");

    const animation = (flowerClass, minSizeVal, maxSizeVal) => {
        const flowerElement = document.createElement("span");
        flowerElement.className = `decorations ${flowerClass}`;
        const minSize = minSizeVal;
        const maxSize = maxSizeVal;
        const size = Math.random() * (maxSize + 1 - minSize) + minSize;
        flowerElement.style.width = `${size}px`;
        flowerElement.style.height = `${size}px`;
        flowerElement.style.left = Math.random() * 100 + '%';
        field.appendChild(flowerElement);

        setTimeout(() => { flowerElement.remove(); }, 8000);
    }
    if(app.$data["feeling"] === 0){
        clearInterval(IntervalHandler);
        IntervalHandler = setInterval(animation.bind(this, "flower",30, 50),500);
        document.querySelector("body").style.backgroundColor = "aqua";
       
    }
    else if(app.$data["feeling"] === 1) {
        clearInterval(IntervalHandler);
        IntervalHandler = setInterval(animation.bind(this, "rose",30, 50),500);
        document.querySelector("body").style.backgroundColor = "#CEF9DC";
    }else if(app.$data["feeling"] === -1){
        clearInterval(IntervalHandler);
        IntervalHandler = setInterval(animation.bind(this, "deadleaf",30, 50),500);
        document.querySelector("body").style.backgroundColor = "#DDDDDD";
    }
}

window.addEventListener("DOMContentLoaded", setAnimation);
window.addEventListener("createdPoem",setAnimation);

let IsPlayed = false;
document.querySelector("html").addEventListener("click",function() {
    if(IsPlayed === false){
        const BGM = new Audio("static/BGM.mp3");
        BGM.volume = 0.05;
        BGM.play();
        
        BGM.addEventListener("ended",function(){
            BGM.currentTime = 0;
            BGM.play();
        })
        IsPlayed = true;
    }
    
})





