function send_quant() { quant_questions.value = position.toString(); }

function simple_quest() {
    position++;
    html.innerHTML += '<h4 id="question'+ position.toString() +'">'+ position.toString() +' - <input size="80" name="question'+ position.toString() +'" /><input name="type'+ position.toString() +'" type="hidden" value="simple" /></h4>';
    send_quant();
}