package hk.edu.polyu.comp.comp2021.simple.model;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.boolValue;
import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.intValue;

/**
 *
 */
public class Unexpr {
    private String expName;
    private String uop;
    private String expRef;
    private int result=-1;
    private boolean result2=false;
    private String resultFlag=null;

    /**
     *
     * @return ;
     */
    public int getInt(){return this.result;}

    /**
     *
     * @return ;
     */
    public String getExpName(){return this.expName;}

    /**
     *
     * @return ;
     */
    public boolean getBool(){return this.result2;}

    /**
     *
     * @return ;
     */
    public String getFlag(){return resultFlag;}

    /**
     *
     * @param expName ;
     * @param uop ;
     * @param expRef ;
     */
    public Unexpr(String expName,String uop,String expRef){
        this.expName=expName;
        this.uop=uop;
        this.expRef=expRef;
    }

    /**
     *
     */
    public void execute(){
        if(uop.equals("~")){
            this.result=-1*intValue(expRef);
            resultFlag="int";
        }
        else if(uop.equals("#")){
            this.result=intValue(expRef);
            resultFlag="int";
        }
        else if(uop.equals("!")){
            this.result2=boolValue(expRef);
            resultFlag="bool";
        }
        else System.out.println("wrong operation");

    }


}
