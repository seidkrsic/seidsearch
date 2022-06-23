
document.addEventListener('DOMContentLoaded', () => { 
    const message = document.querySelector('#close')
    const messageBackground = document.querySelector('#messageBlock')
    if (messageBackground) { 
        message.addEventListener('click', () => { 
            messageBackground.style.display = 'none'
            message.style.display = 'none'
        })
    }

    let searchForm = document.getElementById('searchForm')
    const pageLinks = document.querySelectorAll('#btn')
    // console.log(pageLinks)
    if (searchForm) { 
        pageLinks.forEach( function(btn) { 
            btn.addEventListener('click', function (event) { 
                event.preventDefault()
                let page = btn.dataset.page 
                console.log(page)
                searchForm.innerHTML += `<input value=${page} name='page' hidden/>`
                console.log(searchForm)
                searchForm.submit()
            } )  
            
            
        })
    
    }


    let searchFormProject = document.getElementById('searchFormProject')
    const pageLinksNew = document.querySelectorAll('#btnNew')
    if (searchFormProject) { 

        pageLinksNew.forEach( function(btn) { 
            btn.addEventListener('click', function (event) { 
                event.preventDefault()
                let page = btn.dataset.page
                searchFormProject.innerHTML += `<input value=${page} name='page' hidden/>`
                searchFormProject.submit()
            } )  
            
            
        })
    
        
    }
        
})







    

  
