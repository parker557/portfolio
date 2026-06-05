package hk.edu.polyu.comp.comp2021.simple.model;


import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

/**
 *
 */
public class SimpleInterpreter {
    private static HashMap<String, Vardef> allVardef  = new HashMap<>();

    /**
     *
     * @return ;
     */
    public  static HashMap<String,Vardef> getAllVardef(){return allVardef;}
    private static  HashMap<String, Binexpr> allBexpr = new HashMap<>();

    /**
     *
     * @return ;
     */
    public  static  HashMap<String,Binexpr>getAllBexpr(){return allBexpr;}
    private static  HashMap<String, Print> allPrint = new HashMap<>();

    /**
     *
     * @return ;
     */
    public static  HashMap<String,Print>getAllPrint(){return allPrint;}

    private static HashMap<String, Skip> allSkip = new HashMap<>();

    /**
     *
     * @return ;
     */
    public static HashMap<String,Skip>getAllSkip(){return allSkip;}

    private static  HashMap<String, If> allIf = new HashMap<>();

    /**
     *
     * @return ;
     */
    public static HashMap<String, If> getAllIf(){return allIf;}
    private static  HashMap<String, Unexpr>allUnexpr=new HashMap<>();

    /**
     *
     * @return ;
     */
    public static HashMap<String, Unexpr>getAllUnexpr(){return allUnexpr;}

    private static  HashMap<String, Assign>allAssign=new HashMap<>();

    /**
     *
     * @return ;
     */
    public static HashMap<String,Assign>getAllAssign(){return allAssign;}
    private static  HashMap<String, Loop>allLoop=new HashMap<>();

    /**
     *
     * @return ;
     */
    public static HashMap<String,Loop>getAllLoop(){return allLoop;}
    private static  HashMap<String, Block>allBlock=new HashMap<>();

    /**
     *
     * @return ;
     */
    public static HashMap<String,Block>getAllBlock(){return allBlock;}
    private static  HashMap<String,Program>allProgram=new HashMap<>();

    /**
     *
     * @return ;
     */
    public static HashMap<String,Program>getAllProgram(){return allProgram;}

    /**
     *
     * @param programName ;
     * @param program ;
     */
    public static void addProgram(String programName,Program program){allProgram.put(programName,program);}

    /**
     *
     * @param args ;
     */
    public static void main(String[] args ) {
        new SimpleInterpreter();
    }

    private static ArrayList<String> code=new ArrayList<>();

    /**
     *
      * @param input ;
     */

    public static void codeRead(String input){code.add(input);}

    /**
     *
      * @return ;
     */

    public static ArrayList<String> getCode(){
        return code;
    }

    /**
     *
      */
    public static void clearCode(){code.clear();}
    /**
     *
     */
    private static String cmd = null;

    /**
     *
     * @param input;
     */
    public static void setCmd(String input){
        cmd=input;
    }
    private static boolean flag;

    /**
     *
      * @param a;
     */
    public static void setFlag(boolean a){
        flag=a;
    }
    private static boolean sign_test =false;
    /**
     *
     */

    public SimpleInterpreter(){
        setFlag(true);
        try {
            if (sign_test) {
                switch_case(cmd);

            }
            else {
                while (flag) {
                    System.out.print('>');
                    Scanner sc = new Scanner(System.in);
                    setCmd(sc.nextLine());
                    switch_case(cmd);
                }
            }

        }catch (Exception e){
            System.out.println("Error1,Please try again");
            e.printStackTrace();
            new SimpleInterpreter();
        }
    }


    /**
     *
     * @param cmd;
     * @throws FileNotFoundException;
     */
    public static void switch_case(String cmd) throws FileNotFoundException {
        String[] cmdArr = cmd.split(" ");
        //System.out.println(cmdArr[0]);
        switch (cmdArr[0]) {
            case "vardef":
                Vardef vardef = new Vardef(cmdArr[1], cmdArr[2], cmdArr[3], cmdArr[4]);
                allVardef.put(cmdArr[1], vardef);
                code.add(cmd);
                vardef.execute();
                //System.out.println("@ " + vardef.lab + ":" + vardef.typ + "" + vardef.varName + "=" + cmdArr[4]);
                break;
            case "binexpr":
                Binexpr bexpr = new Binexpr(cmdArr[1], cmdArr[2], cmdArr[3], cmdArr[4]);
                allBexpr.put(cmdArr[1], bexpr);
                code.add(cmd);
                bexpr.execute();

                //System.out.println("@ " + bexpr.expName + ":" + bexpr.expRef1 + " " + bexpr.bop + " " + bexpr.expRef2);
                break;
            case "print":
                Print print = new Print(cmdArr[1], cmdArr[2]);
                code.add(cmd);
                allPrint.put(cmdArr[1], print);
                //System.out.println("@ " + print.lab + ":" + print.expRef);
                break;
            case "skip":
                Skip skip = new Skip(cmdArr[1]);
                code.add(cmd);
                allSkip.put(cmdArr[1], skip);
                //System.out.println("@ " + skip.lab + ":skip");
                break;
            case "if":
                If if1 = new If(cmdArr[1], cmdArr[2], cmdArr[3], cmdArr[4]);
                code.add(cmd);
                allIf.put(cmdArr[1], if1);
                //System.out.println("@ " + if1.lab + " " + if1.expRef + " " + if1.statementLab1 + " " + if1.statementLab2);
                break;
            case "unexpr":
                Unexpr unexpr = new Unexpr(cmdArr[1], cmdArr[2], cmdArr[3]);
                code.add(cmd);
                allUnexpr.put(cmdArr[1], unexpr);
                unexpr.execute();

                //System.out.println("@" + unexpr.expName + " " + unexpr.uop + " " + unexpr.expRef);
                break;
            case "assign":
                Assign assign = new Assign(cmdArr[1], cmdArr[2], cmdArr[3]);
                code.add(cmd);
                allAssign.put(cmdArr[1], assign);
                //System.out.println("@" + assign.lab + " " + assign.varName + " " + assign.expRef);
                break;
            case "while":
                Loop loop = new Loop(cmdArr[1], cmdArr[2], cmdArr[3]);
                code.add(cmd);
                allLoop.put(cmdArr[1], loop);
                //System.out.println("@" + loop.lab + " " + loop.expRef + " " + loop.statement);
                break;
            case "block":
                Block block = new Block(cmdArr[1], cmdArr[2]);
                code.add(cmd);
                int length = cmdArr.length - 3;
                for (int i = 0; i < length; i++) {
                    block.addBlock(cmdArr[i + 3]);
                }
                allBlock.put(cmdArr[1], block);
                //System.out.println("@" + block.lab + " " + block.statementlabs.toString());
                break;
            case "quit":
                flag = false;
                break;
            case "program":
                code.add(cmd);
                Program program = new Program(cmdArr[1], cmdArr[2], code);
                code.clear();
                allProgram.put(cmdArr[1], program);
                break;
            case "execute":
                Execute execute = new Execute(cmdArr[1]);
                execute.execute1();
                flag = false;
                break;
            case "list":
                List list = new List(cmdArr[1]);
                list.execute();
                break;
            case "store":
                Store store = new Store(cmdArr[1], cmdArr[2]);
                store.execute();
                break;
            case "load":
                Load load = new Load(cmdArr[1], cmdArr[2]);
                load.execute();
                break;
            default:
                System.out.println("cmd error,Please try again");
                flag = false;
                new SimpleInterpreter();
                break;
        }


    }

    /**
     *
      * @param input;
     */
    public static void change(String input) {
        setCmd(input);
        sign_test =true;
        new SimpleInterpreter();

    }

    /**
     *
     * @param exp ;
     * @return ;
     */
    public static boolean boolValue(String exp){
        if(!exp.equals("true")&&!exp.equals("false")) {
            for (Map.Entry<String, Binexpr> element : allBexpr.entrySet()) {
                if (element.getValue().getExpName().equals(exp)) {
                    return element.getValue().getBool();
                }
            }
            for (Map.Entry<String, Unexpr> element : allUnexpr.entrySet()) {
                if (element.getValue().getExpName().equals(exp)) {
                    return element.getValue().getBool();
                }
            }
            for (Map.Entry<String, Vardef> element : allVardef.entrySet()) {
                if (element.getValue().getVarName().equals(exp)) {
                    return element.getValue().getBool();
                }
            }
        }

        return Boolean.parseBoolean(exp);
    }


    /**
     *
     * @param exp ;
     * @return ;
     */
    public static int intValue(String exp){

        if(!exp.matches("[0-9]+")) {
            for (Map.Entry<String, Binexpr> element : SimpleInterpreter.allBexpr.entrySet()) {
                if (element.getValue().getExpName().equals(exp)) {
                    return element.getValue().getInt();
                }
            }
            for (Map.Entry<String, Unexpr> element : SimpleInterpreter.allUnexpr.entrySet()) {
                if (element.getValue().getExpName().equals(exp)) {
                    return element.getValue().getInt();
                }
            }
            for (Map.Entry<String, Vardef> element : SimpleInterpreter.allVardef.entrySet()) {
                if (element.getValue().getVarName().equals(exp)) {
                    return element.getValue().getInt();
                }
            }
        }

        return Integer.parseInt(exp);
    }

    /**
     *
     * @param exp ;
     * @return ;
     */
    public static boolean judge(String exp){
        if(!exp.equals("true")&&!exp.equals("false")&&!exp.matches("[0-9]+")) {
            for (Map.Entry<String, Binexpr> element : allBexpr.entrySet()) {
                if (element.getValue().getExpName().equals(exp)) {
                    return element.getValue().getFlag().equals("int");
                }
            }
            for (Map.Entry<String, Unexpr> element : allUnexpr.entrySet()) {
                if (element.getValue().getExpName().equals(exp)) {
                    return element.getValue().getFlag().equals("int");
                }
            }
            for (Map.Entry<String, Vardef> element : allVardef.entrySet()) {
                if (element.getValue().getVarName().equals(exp)) {
                    return element.getValue().getTyp().equals("int");
                }
            }
        }
        else if(exp.equals("true")||exp.equals("false"))return false;

        return true;

    }

}










