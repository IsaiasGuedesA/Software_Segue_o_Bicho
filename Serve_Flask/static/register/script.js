document.getElementById('form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const registro = document.getElementById('registro').value;
    const nome_animal = document.getElementById('nome_animal').value;
    const animal = document.getElementById('animal').value;
    const senha = document.getElementById('senha').value;
    const senhaR = document.getElementById('senhaR').value;
    
    console.log(senhaR)
    console.log(senha)
    if (senhaR != senha)
    {   
        document.getElementById('senhaR').style.border = '2px solid red'
        document.getElementById('senha').style.border = '2px solid red'

    }
    else{
        document.getElementById('senhaR').style.border = 'none'
        document.getElementById('senha').style.border = 'none'

        const jsonData = {
            ANIMAL: animal,
            NOME_ANIMAL: nome_animal,
            REGISTRO: registro,
            SENHA: senha
        }

     
        const response = await fetch('../coleira', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        });
        console.log(jsonData)
        console.log(response.status)
        if(response.status != 200){
            alert("Nao foi possivel adicionar uma coleira com esse registro")
        }
        else{
            window.location.pathname = '/login';
        }
        
        

    }

    // const jsonData = {
    //     name: name,
    //     email: email
    // };
    
})



