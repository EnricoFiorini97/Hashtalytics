var selected = []
const words_list  = document.getElementById("keyword_list")
const del_btn     = document.getElementById("delete-btn")
const del_all_btn = document.getElementById("delete-all-btn")

async function addNewWord() {
    let inputField = document.getElementById('new_word_input')
    let s = inputField.value
    inputField.value = ""

    if (s !== "" && !elements.includes(s)) {
        del_all_btn.disabled = false
        elements.push(s)
        sendUpdatedWords()

        fetch(trend_check_url.format(s)).then((r) => {
            if (r.status === 200)
                trending.push(s)

            addLine(elements.length, s)
        })
    }
}

function initList() {
    for (let i = 0; i < elements.length; i += 1) {
        addLine(i, elements[i])
    }
}

function setSelected(obj) {
    let val = parseInt(obj.value)

    if (selected.includes(val)) {
        selected.splice(selected.indexOf(val), 1)
    } else {
        selected.push(val)
    }

    del_btn.disabled = (selected.length === 0)
}

function deleteSelected() {
    let tmp = []
    selected.forEach((s) => tmp.push(elements[s]))
    tmp.forEach((t) => {
        elements.splice(elements.indexOf(t), 1)
        if (trending.includes(t))
            trending.splice(trending.indexOf(t), 1)
    })

    words_list.textContent = ''
    if (elements.length > 0)
        initList()

    selected = []

    del_btn.disabled = true
    del_all_btn.disabled = (elements.length === 0)

    sendUpdatedWords()
}

function deleteAll() {
    elements = []
    trending = []
    words_list.textContent = ''
    del_btn.disabled = true
    del_all_btn.disabled = true

    sendUpdatedWords()
}

function addLine(id, word) {
    let row_template = document.getElementById("keyword_row")
    let row = row_template.content.firstElementChild.cloneNode(true)
    row.innerHTML = row.innerHTML.format(id, word)

    if (trending.includes(word)) {
        row.classList.add("list-group-item-success")
    }

    words_list.append(row)
}

function sendUpdatedWords() {
    fetch(request_url, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken')
        },
        body: JSON.stringify(elements)
    }).then((r) => console.log("Updated words"))
}