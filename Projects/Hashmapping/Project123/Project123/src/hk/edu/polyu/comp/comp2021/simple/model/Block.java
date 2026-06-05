package hk.edu.polyu.comp.comp2021.simple.model;

import java.util.ArrayList;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.*;

/**
 *
 */
public class Block {
    private final String lab;
    private ArrayList<String> statementlabs=new ArrayList<>();

    /**
     *
     * @param lab ;
     * @param statementlab ;
     */
    public Block(String lab,String statementlab){
        this.lab=lab;
        statementlabs.add(statementlab);
    }

    /**
     *
     * @param s ;
     */
    public void addBlock(String s){
        statementlabs.add(s);
    }

    /**
     *
     * @return ;
     */
    public String getLab() {
        return lab;
    }

    /**
     *
     * @return ;
     */

    /*
    public ArrayList<String> getStatementlabs() {
        return statementlabs;
    }

     */

    /**
     *
     */
    public void execute(){
        for(String lab:statementlabs){
            if(getAllVardef().containsKey(lab)){
                getAllVardef().get(lab).execute();
            }
            else if(getAllAssign().containsKey(lab)){
                getAllAssign().get(lab).execute();
            }

            else if(getAllIf().containsKey(lab)){
                getAllIf().get(lab).execute();
            }
            else if(getAllBlock().containsKey(lab)){
                getAllBlock().get(lab).execute();
            }
            else if(getAllLoop().containsKey(lab)){
                getAllLoop().get(lab).execute();
            }
            else if(getAllPrint().containsKey(lab)){
                getAllPrint().get(lab).execute();
            }

            else if(getAllSkip().containsKey(lab)){
                getAllSkip().get(lab).execute();


            }
        }

    }

}
