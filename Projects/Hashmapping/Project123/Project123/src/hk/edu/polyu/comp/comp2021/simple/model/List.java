package hk.edu.polyu.comp.comp2021.simple.model;

import java.util.Map;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.getAllProgram;

/**
 *
 */
public class List {
    private String programName;

    /**
     *
      * @param programName;
     */
    List(String programName){this.programName=programName;}

    /**
     *
      */
    public void execute(){
        for (Map.Entry<String, Program> element : getAllProgram().entrySet()) {
            if (element.getValue().getProgramName().equals(this.programName)) {
                for(String e:element.getValue().getCommand()){
                    System.out.println(e);
                }
                break;
            }
    }
}
    }
