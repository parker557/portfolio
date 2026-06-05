package hk.edu.polyu.comp.comp2021.simple.model;

import java.util.ArrayList;

/**
 *
 */
public class Program {
    private String programName;
    private String statementLab;

    private ArrayList<String> command=new ArrayList<>();


    /**
     *
      * @return ;
     */
    public ArrayList<String> getCommand(){
        return command;
    }

    /**
     *
     * @return ;
     */
    public String getProgramName(){return programName;}

    /**
     *
     * @return ;
     */
    public String getStatementLab(){return statementLab;}

    /**
     *
     * @param programName ;
     * @param statementLab;
     * @param input;
     */
    Program(String programName,String statementLab,ArrayList<String> input) {
        this.statementLab = statementLab;
        this.programName = programName;
        command.addAll(input);
    }

}
