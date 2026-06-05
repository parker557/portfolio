package hk.edu.polyu.comp.comp2021.simple.model;

import java.util.Map;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.*;

/**
 *
 */
public class Assign {

    private String lab;
    private  String varName;
    private  String expRef;

    /**
     *
     * @param lab ;
     * @param varName ;
     * @param expRef ;
     */
    public Assign(String lab, String varName, String expRef) {
        this.lab = lab;
        this.varName = varName;
        this.expRef = expRef;
    }

    /**
     *
     */
    public void execute() {

        for (Map.Entry<String, Vardef> element : getAllVardef().entrySet()) {
            if (element.getValue().getVarName().equals(this.varName)) {
                if (judge(expRef)) element.getValue().setint(intValue(expRef));
                else element.getValue().setbool(boolValue(expRef));
                break;
            }
        }
        for (Map.Entry<String, Binexpr> element : getAllBexpr().entrySet()) {
            element.getValue().execute();
        }
        for (Map.Entry<String, Unexpr> element : getAllUnexpr().entrySet()) {
            element.getValue().execute();
        }

    }



}

