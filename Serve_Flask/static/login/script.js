document.getElementById('form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const user = document.getElementById('user').value;
    const senha = document.getElementById('senha').value;
   

    // if (senhaR != senha)
    // {   
    //     document.getElementById('senhaR').style.border = '2px solid red'
    //     document.getElementById('senha').style.border = '2px solid red'

    // }
    // else{
    //     document.getElementById('senhaR').style.border = 'none'
    //     document.getElementById('senha').style.border = 'none'

    const jsonData = {
        USER: user,
        SENHA: senha
    }

    
    const response = await fetch('./login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    });

    console.log(jsonData)
    console.log(response)
    console.log(response.redirected)
    console.log(response.url)
    if(response.status != 200){
        alert("Nao foi possivel logar")
    }
    else{
        if(response.redirected){
            window.location.href = response.url;

        }
    }
  
    
        

    

    // const jsonData = {
    //     name: name,
    //     email: email
    // };
    
})



