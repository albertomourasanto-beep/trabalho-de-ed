package luisAlbertoDosSantosOliveira.estoque;

import java.util.ArrayList;

public class Fornecedor {
    private int cnpj;
    private String nome;
    private ArrayList <Produto> itensFornecidos = new ArrayList<Produto>();
    
    public Fornecedor(int cnpj, String nome){
        this.cnpj = cnpj;
        this.nome = nome;
    }
    public void adicionaProduto(Produto p){
        itensFornecidos.add(p);
    }
    public int getCnpj(){ return cnpj;}
    public String getNome(){ return nome;}
    public ArrayList<Produto> getItensFornecidos(){return itensFornecidos;}
}