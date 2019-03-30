function log(what) {
    logs.innerHTML += what + "<br/>";
}

function update(what) {
    var oldTable = document.getElementById('chain'),
        newTable = oldTable.cloneNode(true);
    while (newTable.lastChild) {
        newTable.removeChild(newTable.lastChild);
    }
    for (var i = 0; i < what.chain.length; i++) {
        var tr = document.createElement('tr');
        tr.innerHTML = '<td>' + what.chain[i].index + '</td>' +
            '<td>' + what.chain[i].pow + '</td>' +
            '<td>' + what.chain[i].constraint + '</td>' +
            '<td>' + what.chain[i].timestamp + '</td>' +
            '<td>' + what.chain[i].transactions.length + '</td>';
        newTable.appendChild(tr);
    }
    oldTable.parentNode.replaceChild(newTable, oldTable);
}

let logs = document.getElementById('logs');
let mine = document.getElementById('mine');
let transaction = document.getElementById('transaction');
let register = document.getElementById('register');
let resolve = document.getElementById('resolve');

$.ajax({url: '/', success: update});

mine.addEventListener('click', () => {
    $.ajax({
        url: '/mine', success: update
    });
});

transaction.addEventListener('click', () => {
    $.ajax({
        url: '/transaction/' + document.getElementById('to').value +
            '/' + document.getElementById('amount').value
    });
});