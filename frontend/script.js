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

async function RelatorioPedido() {
    const orderId = document.getElementById('orderid').value;

    if (!orderId) {
        alert('Informe o número do pedido.');
        return;
    }

    try {
        const resposta = await fetch(`http://localhost:5000/pedido/${orderId}`);

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(`Pedido não encontrado: ${dados.erro}`);
        }
        
        const conteudo = dados.mensagem

        const resultado = document.getElementById('resultadoRelatorio');
        const totalGeral = conteudo.itens.reduce((soma, item) => soma + item.total, 0);

        if (conteudo.orderDate == "Não registrado") {
            order_date = conteudo.orderDate
        } else {
            order_date = new Date(conteudo.orderDate).toLocaleDateString()
        }

        resultado.innerHTML = `
            <h3>Pedido ${conteudo.orderId}</h3>
            <p><strong>Data:</strong> ${order_date}</p>
            <p><strong>Cliente:</strong> ${conteudo.customerName}</p>
            <p><strong>Vendedor:</strong> ${conteudo.employeeName}</p>
            <h4>Itens do Pedido:</h4>
            <table border="1" cellpadding="5">
              <thead>
                <tr>
                  <th>Produto</th>
                  <th>Quantidade</th>
                  <th>Preço Unitário</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                ${conteudo.itens.map(item => `
                  <tr>
                    <td>${item.productName}</td>
                    <td>${item.quantity}</td>
                    <td>R$ ${item.unitPrice.toFixed(2)}</td>
                    <td>R$ ${item.total.toFixed(2)}</td>
                  </tr>
                `).join('')}
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="3"><strong>Total Geral:</strong></td>
                  <td><strong>R$ ${totalGeral.toFixed(2)}</strong></td>
                </tr>
              </tfoot>
            </table>
        `;
    } catch (erro) {
        document.getElementById('resultadoRelatorio').innerHTML =
            `<p style="color: red;">Erro: ${erro.message}</p>`;
    }
}

function convertDate(date) {
  const parte = date.split('-');
  return `${parte[0]}-${parte[1]}-${parte[2]}`; 
}

async function RelatorioRanking() {
    const startDate = document.getElementById('startdate').value;
    const endDate = document.getElementById('enddate').value;
  
    if (!startDate || !endDate) {
      alert("Informe as duas datas.");
      return;
    }

    const startDateFormat = convertDate(startDate);
    const endDateFormat = convertDate(endDate);
  
    try {
      const resposta = await fetch(`http://localhost:5000/ranking?start=${startDateFormat}&end=${endDateFormat}`);
      
      const dados = await resposta.json();

      if (!resposta.ok) {
        throw new Error(`Pedido não encontrado: ${dados.erro}`);
      }
    
      const conteudo = dados.mensagem

      const resultado = document.getElementById('resultadoRanking');
      const totalVendido = conteudo.reduce((soma, func) => soma + parseFloat(func.total_vendido), 0);
      const totalVendas = conteudo.reduce((soma, func) => soma + func.total_vendas, 0);
  
      resultado.innerHTML = `
        <h3>Ranking de Vendas</h3>
        <p><strong>Período:</strong> ${startDate} a ${endDate}</p>
        <h4>Funcionários e Vendas:</h4>
        <table border="1" cellpadding="5">
            <thead>
                <tr>
                    <th>Funcionário</th>
                    <th>Total de Vendas</th>
                    <th>Total Vendido (R$)</th>
                </tr>
            </thead>
            <tbody>
                ${conteudo.map(func => `
                    <tr>
                        <td>${func.firstname}</td>
                        <td>${func.total_vendas}</td>
                        <td>R$ ${parseFloat(func.total_vendido).toFixed(2)}</td>
                    </tr>
                `).join('')}
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="2"><strong>Total Geral de Vendas:</strong></td>
                    <td><strong>${totalVendas}</strong></td>
                </tr>
                <tr>
                    <td colspan="2"><strong>Total Vendido (R$):</strong></td>
                    <td><strong>R$ ${totalVendido.toFixed(2)}</strong></td>
                </tr>
            </tfoot>
        </table>
      `;
    } catch (erro) {
      document.getElementById('resultadoRanking').innerHTML = `<p style="color:red;">Erro: ${erro.message}</p>`;
    }
  }  
