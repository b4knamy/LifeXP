var buttonStatus = localStorage.getItem('theme');

if (buttonStatus === 'light') {
    $('body').addClass('light')
    $('.icon').attr('src', '/static/images/sun-theme.png')
};


$('#chk').on('change', () => {
    var currentStatus =  localStorage.getItem('theme');

    if (currentStatus === 'light')  {
        localStorage.setItem('theme', null);
        $('.icon').attr('src', '/static/images/dark-hole-theme.png')
    } else { 
        localStorage.setItem('theme', 'light');
        $('.icon').attr('src', '/static/images/sun-theme.png')
    }
    document.querySelector('body').classList.toggle('light')
    }
);

document.querySelectorAll('.go-to-profile').forEach( (img) => {
    img.addEventListener('click', (event) => {
        event.preventDefault()
        let user_value = img.getAttribute('value');
        
        window.location.href = `/profile/${user_value}`
    } )
} )






function makeComent() {
    document.querySelector('.making-a-comment').style.display = 'block'
}
function hideComent() {
    document.querySelector('.making-a-comment').style.display = 'none'
    document.querySelector('.making-a-comment textarea').value = ''
}

document.querySelectorAll('#cancel-answer-form').forEach( (getAnswerForm) => {
    getAnswerForm.addEventListener('click', () => {
        formElement = getAnswerForm.closest('.answer-full-interact-coments').lastElementChild
        formElement.style.display = 'none'
    })
})

document.querySelectorAll('#show-answer-form').forEach( (getAnswerForm) => {
    getAnswerForm.addEventListener('click', () => {
        formElement = getAnswerForm.closest('.answer-full-interact-coments').lastElementChild
        formElement.style.display = 'flex'
    })
})

document.querySelectorAll('#edit-post').forEach((button) => {
    button.addEventListener('click', (event) => {
        let dadDiv = event.target.closest('#subanswer-content');
        let formContainer = event.target.closest('#father-user-container').lastChild.previousElementSibling;
        let content = dadDiv.querySelector('.text-class-get').textContent.trim()

        dadDiv.style.display = 'none';
        formContainer.children[0].value = content
        formContainer.style.display = 'flex';
    })
})
document.querySelectorAll('#cancel-edit-post').forEach((button) => {
    button.addEventListener('click', (event) => {
        let formContainer = event.target.closest('#editing-answer')
        let dadDivList = event.target.closest('#father-user-container').children
        let dadDiv = dadDivList[dadDivList.length - 2]
        console.log(dadDiv)
        formContainer.style.display = 'none';
        dadDiv.style.display = 'flex';
    })
})


document.querySelectorAll('.follow').forEach( (current_obj) => {current_obj.addEventListener('click', (event) => {
    event.preventDefault();
    const xhttp = new XMLHttpRequest();
    var identifier = event.target.getAttribute('value')

    let value = event.target.textContent

    xhttp.onload = () => {
        if (value == "Seguindo") {
            event.target.textContent = 'Seguir';
            event.target.setAttribute('title', 'Você não segue esse usuário!')
            
        } else {
            event.target.textContent = 'Seguindo';
            event.target.setAttribute('title', 'Você já está seguindo esse usuário!')
            
    }}

    xhttp.open('POST', `follow/${identifier}`);
    xhttp.send()})
})

document.querySelectorAll('.answer-user-profile i').forEach((icon) => {
    icon.addEventListener('click', () => {
        let fatherDiv = icon.closest('.answer-full-interact-coments')
        let hide_answer = fatherDiv.children[1]
        let show_answers = fatherDiv.children[0]

        if (hide_answer.style.display === 'none') {

            show_answers.querySelector('.line-separator-x-first').style.display = 'block'
            hide_answer.style.display = 'flex'
            icon.style.transform = 'rotate(180deg)'
        } else {
            show_answers.querySelector('.line-separator-x-first').style.display = 'none'
            hide_answer.style.display = 'none'
            icon.style.transform = 'rotate(360deg)'
        }
        
})
})

var all_p = document.querySelectorAll('.text-class-get')
for (var i = 0, j = all_p.length; i < j; i++) {
    let p = all_p[i] 
    if (p.innerHTML.length > 900) {
        var new_span = document.createElement('span')
        new_span.setAttribute('id', 'span-seemore')
        new_span.innerHTML = '... Ver mais'
        if (p.id == 'hpc-content-child') {
            var pDad = p.closest('.hpc-content')
            new_span.style.background = 'darkgray'
        } else {
            var pDad = p.closest('.a-u-c-t')
        }
        pDad.style.maxHeight = '350px'
        new_span.style.right ='0';
        new_span.style.bottom = '0';
        pDad.appendChild(new_span)   
    }
}

function changePost() {
    document.getElementById('update').showModal()
}


document.querySelectorAll('#span-seemore').forEach((span) => {
    span.addEventListener('click', () => {
        if (span.parentElement.firstElementChild.id == 'hpc-content-child') {
            var dad_span = span.closest('.hpc-content');
        } else {
            var dad_span = span.closest('.a-u-c-t')
        }
        console.log(span)
        console.log(dad_span)
        if (span.innerHTML === '... Ver menos') {
            span.innerHTML = '... Ver mais';
            span.style.position = 'absolute'
            console.log(span.style.position)
            span.style.right ='0';
            span.style.bottom = '0';
            dad_span.style.maxHeight = '350px';
        } else {
        dad_span.style.maxHeight = 'none';
        span.style.position = 'relative'
        console.log(span.style.position)
        span.style.right ='none';
        span.style.bottom = 'none';
        span.innerHTML = '... Ver menos';
    }
    })
})


document.querySelectorAll('#like').forEach( (like) => {
    like.addEventListener('click', (event) => {
        event.preventDefault();
        const xhttp_like = new XMLHttpRequest();
        let identifier = like.getAttribute('name');
        xhttp_like.onload = () => {
            if (like.firstChild.id === 'got-clicked') {
            like.firstChild.removeAttribute('id')
            } else {
                like.firstChild.setAttribute('id', 'got-clicked')
            }
        }
        xhttp_like.open('POST', `lod/${identifier}/like`);
        xhttp_like.send()
        }
    )
})





document.querySelectorAll('#dislike').forEach( (unlike) => {
    unlike.addEventListener('click', (event) => {
        event.preventDefault();
        const xhttp_unlike = new XMLHttpRequest();
        let identifier = unlike.getAttribute('name');

        xhttp_unlike.onload = () => {
            if (unlike.firstChild.id === 'got-clicked') {
                unlike.firstChild.removeAttribute('id')
            } else {
                unlike.firstChild.setAttribute('id', 'got-clicked')
            }
        }

        xhttp_unlike.open('POST', `lod/${identifier}/dislike`);
        xhttp_unlike.send()
        }
    )
})


document.querySelectorAll('.select-each-image').forEach( (img) => {
    
    img.addEventListener('click', (event) => {
        event.preventDefault();
        changeColorImg()
        event.target.style.boxShadow = '0 0 30px red';
        let current_img =event.target.getAttribute('value')
        document.getElementById('send-image').setAttribute('value', current_img)
        
    })
})
function changeImg() {
    let name = document.getElementById('send-image').value

    console.log(document.getElementById('current-image'))
    document.getElementById('current-image').setAttribute('src', `/static/images/${name}.jpg`)
    document.querySelector('.show-image-options').style.display = 'none'
}

function changeColorImg() {
    document.querySelectorAll('.select-each-image').forEach( (img) => {
            img.style.boxShadow = '0 0 15px black';
        })
    }

function closeShowImg() {
    document.querySelector('.show-image-options').style.display = 'none'
}
function showShowImg() {
    document.querySelector('.show-image-options').style.display = 'flex'
}


document.getElementById('save-post-btn').addEventListener('click', (event) => {
    event.preventDefault()
    try {
        let save_request = new XMLHttpRequest()

        save_request.onload = () => {
            if (event.target.textContent === 'Salvar') {
                event.target.textContent = 'Salvo'
            } else {
                event.target.textContent = 'Salvar'
            }
        }
        save_request.open('POST', `save_post/${event.target.getAttribute('value')}`)
        save_request.send()
    }
    catch(error) {
        console.log(error, 'AAAAAAAAAAA')
    }
} )