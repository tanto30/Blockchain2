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
    $.ajax({url: '/balance', success: updateBalance});
}

function updateBalance(what) {
    balance.innerText = what;
}

let logs = document.getElementById('logs');
let mine = document.getElementById('mine');
let transaction = document.getElementById('transaction');
let register = document.getElementById('register');
let resolve = document.getElementById('resolve');
let controlbtn = document.getElementById('controlbtn');
let logsbtn = document.getElementById('logsbtn');
let databtn = document.getElementById('databtn');
let balance = document.getElementById('balance');

$.ajax({url: '/', success: update});

document.getElementById('control').hidden = false;
document.getElementById('logs').hidden = true;
document.getElementById('data').hidden = true;

mine.addEventListener('click', () => {
    $.ajax({
        url: '/mine', success: update
    });
    log("Sent mine request");
});

transaction.addEventListener('click', () => {
    let to = document.getElementById('to').value;
    let amount = document.getElementById('amount').value;
    if (!to || !amount) {
        log("Error: to and amount are required");
        return;
    }
    $.ajax({
        url: '/transaction/' + to + '/' + amount
    });
    log("Sent transaction request to " + to + " amount: " + amount);
});

register.addEventListener('click', () => {
    let port = document.getElementById('port').value;
    if (!port) {
        log("Error: port is required");
        return;
    }
    $.ajax({
        url: port
    });
    log("Registered node with port " + port);
});

resolve.addEventListener('click', () => {
    $.ajax({
        url: '/resolve'
    });
    log("Sent resolve request");
});

controlbtn.addEventListener('click', () => {
    document.getElementById('control').hidden = false;
    document.getElementById('logs').hidden = true;
    document.getElementById('data').hidden = true;
});

logsbtn.addEventListener('click', () => {
    document.getElementById('control').hidden = true;
    document.getElementById('logs').hidden = false;
    document.getElementById('data').hidden = true;
});

databtn.addEventListener('click', () => {
    document.getElementById('control').hidden = true;
    document.getElementById('logs').hidden = true;
    document.getElementById('data').hidden = false;
});