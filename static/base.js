let del = document.getElementsByClassName('delete');
[...del].forEach(element => {
    element.addEventListener('click', () => {

        element.parentNode.classList.add('remove')
        
    });
});


let message = document.getElementsByClassName('message');
[...message].forEach(element=>{
    console.log(element)
    setTimeout(()=>{
        element.parentNode.classList.add('remove')
    },5000)
})