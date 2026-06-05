package hk.edu.polyu.comp.comp2021.simple.model;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.*;

/**
 *
 */
public class Print {
    private String lab;
    private String expRef;

    /**
     *
     * @param name ;
     * @param expRef ;
     */

    public Print(String name, String expRef) {
        this.lab = name;
        this.expRef = expRef;
    }

    /**
     *
     */
    public void execute() {
        if (judge(expRef)) System.out.println(intValue(expRef));
        else System.out.println(boolValue(expRef));


    }

}

