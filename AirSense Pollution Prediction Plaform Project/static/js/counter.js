const counters=document.querySelectorAll(".counter");

counters.forEach(counter=>{

    const target=Number(counter.innerText);

    let count=0;

    const speed=30;

    const update=()=>{

        if(count<target){

            count+=target/80;

            counter.innerText=Math.ceil(count);

            setTimeout(update,speed);

        }

        else{

            counter.innerText=target;

        }

    }

    update();

});