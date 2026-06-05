package hk.edu.polyu.comp.comp2021.simple.model;

import java.io.FileReader;
import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

/**
 *
 */
public class Load {
    private String programName;
    private String path;

    /**
     *
      * @param programName ;
     * @param path ;
     */
    Load(String programName,String path){
        this.programName=programName;
        this.path=path;
    }

    /**
     *
      * @throws FileNotFoundException ;
     */
    public void execute() throws FileNotFoundException {
        ArrayList<String> command=new ArrayList<>();

        String fileName = path+".txt";
            try (Scanner sc = new Scanner(new FileReader(fileName))) {
                while (sc.hasNextLine()) {
                    command.add(sc.nextLine()) ;
                }
                int length=command.size();
                String last[] =command.get(length-1).split(" ");

                Program program=new Program(programName,last[2],command);
                SimpleInterpreter.addProgram(programName,program);
            }

    }

}
