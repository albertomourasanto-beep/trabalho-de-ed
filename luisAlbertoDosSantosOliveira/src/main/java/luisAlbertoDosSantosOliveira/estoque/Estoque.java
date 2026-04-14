package luisAlbertoDosSantosOliveira.estoque;

import java.util.ArrayList;
import java.util.Date;

public class Estoque{
    private ArrayList<Produto> produtos = new ArrayList<Produto>();
    public void incluir(Produto p) {
        if(buscarPorCodigo(p.getCodigo()) != null){
            System.out.println("Produto já existente.");
        }
        else{
            produtos.add(p);
        }
    }
    public void comprar(int cod, int quant, double preco){
        Produto p=buscarPorCodigo(cod);
        if (p == null){
            System.out.println("Produto inexistente.");
            return ;
        }
        p.compra(quant,preco);
    }
    public double vender(int cod, int quant){
        Produto p = buscarPorCodigo(cod);
        if (p == null){
            System.out.println("Produto inexistente.");
            return -1;
        }
        double val=p.venda(quant);
        return val;
    }
    public int quantidade(int cod){
        Produto p = buscarPorCodigo(cod);
        if (p == null){
            System.out.println("Produto inexistente.");
            return -1;
        }
        int quant=p.getQuantidade();
        return quant;
    }
    public ArrayList<Fornecedor> fornecedores(int cod){
        Produto p = buscarPorCodigo(cod);
        if(p == null) return null ;
        return p.getFornecedores();
    }
    public ArrayList<Produto> estoqueAbaixoDoMinimo(){
        ArrayList<Produto> abaixoDoMinimo = new ArrayList<Produto>();
        for(Produto p : produtos){
            if(p.getQuantidade()< p.getEstoqueMinimo()) abaixoDoMinimo.add(p);
        }
        return abaixoDoMinimo;
    }
    public void adicionarFornecedor(int cod, Fornecedor f){
        Produto p = buscarPorCodigo(cod);
        if(p== null) return ;
        p.adicionarFornecedor(f);
    }
    public double precoDeVenda(int cod){
        Produto p = buscarPorCodigo(cod);
        if (p == null){
            System.out.println("Produto inexistente.");
            return -1 ;
        }
        double val= p.getPrecoVenda();
        return val;
    }
    public double precoDeCompra(int cod){
        Produto p = buscarPorCodigo(cod);
        if (p == null){
            System.out.println("Produto inexistente.");
            return -1;
        }
        double val= p.getPrecoCompra();
        return val;
    }
    private Produto buscarPorCodigo(int cod){
        for(Produto p : produtos){
            if (p.getCodigo()==cod){
                return p;
            }
        }
        return null;
    }
    public String movimentacao(int cod, Date inicio, Date fim) {
        Produto p = buscarPorCodigo(cod);
        if (p == null) return null;

        String resultado = "";

        for (Movimentacao m : p.getMovimentacoes()) {
            // filtra só as que estão entre inicio e fim
            if (!m.getData().before(inicio) && m.getData().before(fim)) {
                int dia = m.getData().getDate();
                int mes = m.getData().getMonth() + 1;
                int ano = m.getData().getYear() + 1900;

                resultado += "Data: " + dia + "/" + mes + "/" + ano
                        + ". " + m.getTipo()
                        + ". Valor: " + m.getValor()
                        + ". Quantidade: " + m.getQuantidade()
                        + ".\n";
            }
        }
        return resultado;
    }
}