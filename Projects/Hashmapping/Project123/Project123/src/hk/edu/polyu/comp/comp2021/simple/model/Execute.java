package hk.edu.polyu.comp.comp2021.simple.model;

import java.util.Map;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.*;

/**
 *
 */
public class Execute {
    private String programName;

    /**
     *
     * @param programName ;
     */
    Execute(String programName) {
        this.programName = programName;
    }

    /**
     *
     */
    void execute1() {
        for (Map.Entry<String, Program> element : getAllProgram().entrySet()) {
            if (element.getValue().getProgramName().equals(this.programName)) {
                for (Map.Entry<String, Block> elementBl : getAllBlock().entrySet()) {
                    if (element.getValue().getStatementLab().equals(elementBl.getValue().getLab())) {
                        elementBl.getValue().execute();
                        break;
                    }
                }
                break;
            }
        }
    }

}

