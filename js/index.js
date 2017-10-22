const QUESTION_INPUT = /** @type {HTMLInputElement} */(document.querySelector("#question"));
const SEND_BUTTON = /** @type {HTMLButtonElement} */(document.querySelector("#send"));
const SEARCH_INTERFACE = /** @type {HTMLButtonElement} */(document.querySelector("#search"));
const ARTICLE_INTERFACE = /** @type {HTMLButtonElement} */(document.querySelector("#article"));
const CHAT_INTERFACE = /** @type {HTMLButtonElement} */(document.querySelector("#chat"));

let ws = new WebSocket("ws://localhost:8000");

// Close socket when window closes
$(window).on('beforeunload', function(){
    ws.close();
});

ws.onerror = function(event) {
    location.reload();
}

ws.onmessage = function(event)  { 
    let message_received = event.data;
    if (typeof message_received === 'object') {

    } else {
        addBotMessage(message_received);
    }
};

/**
 * @property {number} currentPage
 */
let state = {
    question: "",
    messages: [],
    mode: "search",
    suggestions: []
};

function createElem(name, value, className) {
    let elem = document.createElement(name);
    elem.textContent = value;
    if(value) {
        elem.id = value;
    }
    if (className) {
        elem.className = className;
    }
    return elem;
}

function render(state) {
    let suggestionsBox = document.querySelector(".suggestions");
    SEND_BUTTON.disabled = !state.question;
    suggestionsBox.textContent = "";
    CHAT_INTERFACE.textContent = "";

    if (state.mode == "search") {
        for (let i = 0; i < state.suggestions.length; i++) {
            suggestionsBox.appendChild(createElem("div", state.suggestions[i], "col-11 suggestion"));
        }
    
        let suggestionDivs = document.querySelectorAll(".suggestion");
        for(let i = 0; i < suggestionDivs.length; i++) {
            suggestionDivs[i].addEventListener('click', goToArticle);
        }
    } else if (state.mode == "article") {
        SEARCH_INTERFACE.classList.add("disappear");
        ARTICLE_INTERFACE.classList.add("appear");
        ARTICLE_INTERFACE.classList.remove("d-none");
    } else if (state.mode == "chat") {
        state.messages.forEach(function(element) {
            if(element.from == "user") {
                addUserMessage(element.message);
            } else {
                addBotMessage(element.message);
            }
        });
    }
}

render(state);

QUESTION_INPUT.addEventListener("input", function() {
    let q = QUESTION_INPUT.value.trim().toLocaleLowerCase();
    
    state.question = q;
    state.suggestions = q? ["What is sex?", "What is gender?", "What is orientation?"] : [];
    render(state);
})

SEND_BUTTON.addEventListener("click", function() {
    if(QUESTION_INPUT.value) {
        if(state.mode !== "chat") {
            state.mode = "chat";
            ws.send(999);
        }
        state.messages.push({from: "user", message: QUESTION_INPUT.value.trim()});
        QUESTION_INPUT.value = "";
        render(state);
    }
});

function goToArticle(t) {
    //alert(t.target.id);
    //TODO Get article details
    state.mode = "article";
    render(state);
}

function addUserMessage(message) {
    let elem = createElem("div", "", "row");
    let elem2 = createElem("div", "", "col-2")
    elem2.appendChild(createElem("div", "", "userIcon"))
    elem.appendChild(createElem("div", "", "col-1"));
    elem.appendChild(createElem("div", message, "col-9 message text-right"));
    elem.appendChild(elem2);
    CHAT_INTERFACE.appendChild(elem);
}

function addBotMessage(message) {
    let elem = createElem("div", "", "row");
    let elem2 = createElem("div", "", "col-2")
    elem2.appendChild(createElem("div", "", "responseIcon"));
    elem.appendChild(elem2);
    elem.appendChild(createElem("div", message, "col-9 message text-right"));
    CHAT_INTERFACE.appendChild(elem);
}