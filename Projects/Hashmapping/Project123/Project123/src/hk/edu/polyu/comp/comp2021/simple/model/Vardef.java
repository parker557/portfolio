package hk.edu.polyu.comp.comp2021.simple.model;

import hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter;

/**
 *
 */
public class Vardef {
    private String lab;
    private String typ;

    private String varName;
    private String expRef;

    private int result=0;

    private boolean result2=false;

    /**
     *
      * @return ;
     */
    public String getVarName(){return varName;}

    /**
     *
      * @return
     */
    /**
     *
     * @return ;
     */
    public String getTyp(){return typ;}

    /**
     *
     * @return ;
     */
    public int getInt(){return result;}

    /**
     *
     * @return ;
     */
    public boolean getBool(){return result2;}


//将输入的的type Sting识别为不同类别（int or boolean）并将后面的expRef 的String
// 保存在element的不同result中（int －－ element。result，boolean －－ element。result2）

    /**
     *
      * @param lab ;
     * @param typ ;
     * @param varName ;
     * @param expRef ;
     */
    public Vardef(String lab, String typ,String varName, String expRef) {
        this.lab = lab;
        this.typ = typ;
        this.varName = varName;
        this.expRef = expRef;
    }

    /**
     *
     * @param x ;
     */

    public void setint(int x){
        this.result=x;
    }

    /**
     *
      * @param x ;
     */
    public void setbool(boolean x){
        this.result2=x;
    }

    /**
     *
      */
    public void execute(){
        if(typ.equals("int"))result= SimpleInterpreter.intValue(expRef);
        else if(typ.equals("bool"))result2=SimpleInterpreter.boolValue(expRef);
        else System.out.println("wrong type");

    }

}
