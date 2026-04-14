package luisAlbertoDosSantosOliveira.estoque;
import java.util.ArrayList;
public class Produto {
    private int codigo;
    private String descricao;
    private double precoCompra;
    private double precoVenda;
    private double lucro;
    private int quantidade;
    private int estoqueMinimo;
    private ArrayList<Fornecedor> fornecedores = new ArrayList<Fornecedor>();
    private ArrayList<Movimentacao> movimentacoes = new ArrayList<Movimentacao>();


    public Produto(int cod, String desc, int min, double lucro){
        this.codigo = cod;
        this.descricao = desc;
        this.estoqueMinimo = min;
        this.lucro = lucro;
        this.quantidade = 0;
        this.precoCompra = 0;
        this.precoVenda = 0;
    }
    public void adicionarFornecedor(Fornecedor f) {
        fornecedores.add(f);
    }
    public void compra(int quant, double val){
        if (quant <=0 || val<=0) return;
        
        this.precoCompra = (this.quantidade * this.precoCompra + quant*val) / (this.quantidade + quant);

        this.precoVenda=this.precoCompra * (1+this.lucro);
        
        this.quantidade+=quant;

        movimentacoes.add(new Movimentacao("Compra", val, quant));
    }
    public double venda (int quant) {
        if (quant <=0) return -1;
        if (quant>this.quantidade) return-1;
        this.quantidade -=quant;
        movimentacoes.add(new Movimentacao("Venda", this.precoVenda, quant));
        return quant * this.precoVenda;
    }
    public int getCodigo() { return codigo; }
    public String getDescricao() { return descricao; }
    public double getPrecoCompra() { return precoCompra; }
    public double getPrecoVenda() { return precoVenda; }
    public int getQuantidade() { return quantidade; }
    public int getEstoqueMinimo() { return estoqueMinimo; }
    public ArrayList<Fornecedor> getFornecedores() {
    return fornecedores; }
    public ArrayList<Movimentacao> getMovimentacoes() { return movimentacoes; }
    @Override
    public String toString() {
        return "Produto: " + descricao + " | Código: " + codigo + " | Quantidade: " + quantidade;
    }
}