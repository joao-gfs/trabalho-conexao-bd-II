const produtos = [];

function adicionarProduto() {
    const productid = parseInt(document.getElementById('productid').value);
    const quantity = parseInt(document.getElementById('quantity').value);

    if (!productid || !quantity) {
        alert("Preencha todos os campos do produto.");
        return;
    }

    const produto = { productid, quantity };
    produtos.push(produto);
    renderizarProdutos();

    document.getElementById('productid').value = '';
    document.getElementById('quantity').value = '';
}

function removerProduto(index) {
    produtos.splice(index, 1);
    renderizarProdutos();
}

function renderizarProdutos() {
    const lista = document.getElementById('listaProdutos');
    lista.innerHTML = '';

    produtos.forEach((prod, index) => {
        const div = document.createElement('div');
        div.className = 'produto-item';
        div.innerHTML = `
            <span>Produto: ${prod.productid} - Quantidade: ${prod.quantity}</span>
            <button type="button" onclick="removerProduto(${index})">X</button>
        `;
        lista.appendChild(div);
    });
}

document.getElementById('pedidoForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const orderid = parseInt(document.getElementById('orderid').value);
    const customerid = document.getElementById('customerid').value.trim();
    const employeename = document.getElementById('employeename').value.trim();

    if (!orderid || !customerid || !employeename || produtos.length === 0) {
        alert("Preencha todos os campos e adicione pelo menos um produto.");
        return;
    }

    const pedido = {
        orderid,
        customerid,
        employeename,
        produtos
    };

    try {
        const response = await fetch('http://localhost:5000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(pedido)
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.mensagem);
            window.location.reload();
        } else {
            alert(data.erro);
        }
    } catch (err) {
        console.error(err);
        alert("Erro de conexão com o backend.");
    }
});
