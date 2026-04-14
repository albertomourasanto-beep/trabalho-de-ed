package luisAlbertoDosSantosOliveira.estoque;

import java.util.Date;

public class Movimentacao {
    private Date data;
    private String tipo; // "Compra" ou "Venda"
    private double valor;
    private int quantidade;

    public Movimentacao(String tipo, double valor, int quantidade) {
        this.data = new Date(); // pega a data/hora atual
        this.tipo = tipo;
        this.valor = valor;
        this.quantidade = quantidade;
    }

    public Date getData() { return data; }
    public String getTipo() { return tipo; }
    public double getValor() { return valor; }
    public int getQuantidade() { return quantidade; }
}