package hk.edu.polyu.comp.comp2021.simple.model;
import hk.edu.polyu.comp.comp2021.simple.model.Program;

import java.io.BufferedWriter;
import java.io.*;
import java.util.Map;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.getAllProgram;

/**
 *
 */
public class Store {
   private String programName;
    private String path;

    /**
     *
      * @param programName ;
     * @param path ;
     */
    Store(String programName,String path){
        this.path=path;
        this.programName=programName;
    }

    /**
     *
      */
    public void execute(){
        BufferedWriter writer = null;
        File file = new File(path+ programName + ".txt");
        //如果文件不存在，则新建一个
        if(!file.exists()){
            try {
                file.createNewFile();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        //写入
        try {
            writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file,false), "UTF-8"));
            for (Map.Entry<String, Program> element : getAllProgram().entrySet()) {
                if (element.getValue().getProgramName().equals(this.programName)){
                    for(String e:element.getValue().getCommand()){
                        writer.write(e+"\n");
                    }
                    break;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            try {
                if(writer != null){
                    writer.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        System.out.println("文件写入成功！");


    }
}
