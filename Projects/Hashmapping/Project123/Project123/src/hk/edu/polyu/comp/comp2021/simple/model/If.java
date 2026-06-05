package hk.edu.polyu.comp.comp2021.simple.model;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.*;

/**
 *
 */
public class If {
    private String lab;
    private String expRef;
    private String statementLab1;
    private String statementLab2;

    /**
     *
     * @param name ;
     * @param expRef ;
     * @param statement1 ;
     * @param statement2 ;
     */
    public If(String name, String expRef, String statement1, String statement2) {
        this.lab = name;
        this.expRef = expRef;
        this.statementLab1 = statement1;
        this.statementLab2 = statement2;
    }

    /**
     *
     */
    public void execute(){

        if(boolValue(expRef)){
            if(getAllVardef().containsKey(statementLab1)){
                getAllVardef().get(statementLab1).execute();
            }
            else if(getAllAssign().containsKey(statementLab1)){
                getAllAssign().get(statementLab1).execute();
            }

            else if(getAllIf().containsKey(statementLab1)){
                getAllIf().get(statementLab1).execute();
            }
            else if(getAllBlock().containsKey(statementLab1)){
                getAllBlock().get(statementLab1).execute();
            }
            else if(getAllLoop().containsKey(statementLab1)){
                getAllLoop().get(statementLab1).execute();
            }
            else if(getAllPrint().containsKey(statementLab1)){
                getAllPrint().get(statementLab1).execute();
            }

            else if(getAllSkip().containsKey(statementLab1)){
                getAllSkip().get(statementLab1).execute();
            }
        }
        else {
            if(getAllVardef().containsKey(statementLab2)){
                getAllVardef().get(statementLab2).execute();
            }
            else if(getAllAssign().containsKey(statementLab2)){
                getAllAssign().get(statementLab2).execute();
            }

            else if(getAllIf().containsKey(statementLab2)){
                getAllIf().get(statementLab2).execute();
            }
            else if(getAllBlock().containsKey(statementLab2)){
                getAllBlock().get(statementLab2).execute();
            }
            else if(getAllLoop().containsKey(statementLab2)){
                getAllLoop().get(statementLab2).execute();
            }
            else if(getAllPrint().containsKey(statementLab2)){
                getAllPrint().get(statementLab2).execute();
            }

            else if(getAllSkip().containsKey(statementLab2)){
                getAllSkip().get(statementLab2).execute();
            }


        }


    }

}
