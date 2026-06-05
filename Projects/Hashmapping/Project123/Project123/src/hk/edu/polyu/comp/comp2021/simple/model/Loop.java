package hk.edu.polyu.comp.comp2021.simple.model;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.*;

/**
 *
 */
public class Loop {
    private String lab;
    private String statement;
    private String expRef;

    /**
     *
     * @param lab ;
     * @param expRef ;
     * @param statement ;
     */
    public Loop(String lab,String expRef,String statement) {
        this.lab = lab;
        this.statement = statement;
        this.expRef = expRef;
    }

    /**
     *
     */
    public void execute(){
        while(boolValue(expRef)){

             if(getAllAssign().containsKey(statement)){
                getAllAssign().get(statement).execute();
            }

            else if(getAllIf().containsKey(statement)){
                getAllIf().get(statement).execute();
            }
            else if(getAllBlock().containsKey(statement)){
                getAllBlock().get(statement).execute();
            }
            else if(getAllLoop().containsKey(statement)){
                getAllLoop().get(statement).execute();
            }

        }


    }

}
