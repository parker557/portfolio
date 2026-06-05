package hk.edu.polyu.comp.comp2021.simple.model;

import static hk.edu.polyu.comp.comp2021.simple.model.SimpleInterpreter.*;

/**
 *
 */
public class Binexpr {
    private String expName;
    private String expRef1;
    private String expRef2;
    private String bop;

    private boolean result2 = false;
    private int result = -1;

    private String resultFlag = null;//bool means the result is boolean; int means result is int

    /**
     *
     * @return ;
     */
    public String getFlag(){return resultFlag;}

    /**
     *
     * @return ;
     */
    public String getExpName(){return expName;}

    /**
     *
     * @return ;
     */
    public boolean getBool(){return this.result2;}

    /**
     *
     * @return ;
     */
    public int getInt(){return this.result;}

    /**
     *
     * @param expName ;
     * @param expRef1 ;
     * @param bop ;
     * @param expRef2 ;
     */
    public Binexpr(String expName, String expRef1, String bop, String expRef2) {
        this.expName = expName;
        this.expRef1 = expRef1;
        this.expRef2 = expRef2;
        this.bop = bop;
    }
//分不同种情况，同样，将结果储存在element.result（int）和element.result2（boolean）中。
// 并运用变量resultflag来储存结果的类型

    /**
     *
     */
    public void execute() {
        if (bop.equals("+") || bop.equals("-") || bop.equals("*") || bop.equals("/") || bop.equals("%")) {
            switch (bop) {
                case "+":
                    this.result = intValue(expRef2) + intValue(expRef1);
                    break;
                case "-":
                    this.result = intValue(expRef1) - intValue(expRef2);
                    break;
                case "*":
                    this.result = intValue(expRef1) * intValue(expRef2);
                    break;
                case "/":
                    if (intValue(expRef2) == 0) {
                        System.out.println("cannot / 0");
                        break;
                    }
                    this.result = intValue(expRef1) / intValue(expRef2);
                    break;
                case "%":
                    if (intValue(expRef2) == 0) {
                        System.out.println("cannot % 0");
                        break;
                    }
                    this.result = intValue(expRef1) % intValue(expRef2);
                    break;
            }
            this.resultFlag = "int";


        } else if (bop.equals("!=") || bop.equals(">") || bop.equals("<") || bop.equals(">=") || bop.equals("<=") || bop.equals("==")) {
            if (judge(expRef2) == judge(expRef1)) {
                if (judge(expRef1)) {
                    switch (bop) {
                        case "!=":
                            this.result2 = intValue(expRef1) != intValue(expRef2);
                            break;
                        case "==":
                            this.result2 = intValue(expRef1) == intValue(expRef2);
                            break;
                        case ">":
                            this.result2 = intValue(expRef1) > intValue(expRef2);
                            break;
                        case "<":
                            this.result2 = intValue(expRef1) < intValue(expRef2);
                            break;
                        case ">=":
                            this.result2 = intValue(expRef1) >= intValue(expRef2);
                            break;
                        case "<=":
                            this.result2 = intValue(expRef1) <= intValue(expRef2);
                            break;
                    }
                    resultFlag = "bool";
                } else if (!judge(expRef1) && !(bop.equals(">") || bop.equals("<") || bop.equals(">=") || bop.equals("<="))) {
                    switch (bop) {
                        case "!=":
                            this.result2 = boolValue(expRef1) != boolValue(expRef2);
                            break;
                        case "==":
                            this.result2 = boolValue(expRef1) == boolValue(expRef2);
                            break;

                    }
                    resultFlag = "bool";
                } else System.out.println("operation not match");
            } else System.out.println("type not match");
        } else if (bop.equals("||") || bop.equals("&&")) {
            if (bop.equals("||")) this.result2 = boolValue(expRef1) || boolValue(expRef2);
            else this.result2 = boolValue(expRef1) && boolValue(expRef2);
            resultFlag = "bool";
        } else System.out.println("wrong operation");

    }


}
